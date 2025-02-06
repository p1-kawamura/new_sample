from django.shortcuts import render,redirect
from zaiko.models import Size,Shouhin,Category,Rental,Label,Rireki_rental,Rireki_shouhin
from django.http import JsonResponse
import json
from django.db.models import Max
from django.contrib.auth.decorators import login_required
import datetime
import csv
from django.http import HttpResponse
import urllib.parse
import requests


@login_required
def index2(request):
    comment=request.session["comment"]
    size_cnt=Size.objects.filter(size_num=0).count()
    #user認証
    kanri=0
    if request.user.username == "p1masao":
        kanri=1
    params={
        "ins":Category.objects.all().order_by("category_num"),
        "sizes":Size.objects.all().order_by("size_num"),
        "label":Label.objects.all().count(),
        "comment":comment,
        "kanri":kanri,
        "size_cnt":size_cnt,
    }
    return render(request,"zaiko2/index2.html",params)


# カテゴリクリック
def category_click_ajax(request):
    category=request.POST.get("category")
    if category == "取寄せ":
        items=list(Shouhin.objects.filter(sample_num = "", status=0).values())
        hinban=Shouhin.objects.filter(sample_num = "", status=0)
    else:
        items=list(Shouhin.objects.filter(category=category, status=0).values())
        hinban=Shouhin.objects.filter(category=category, status=0)
    hinban_list=[]
    for i in hinban:
        if i.shouhin_num not in hinban_list:
            hinban_list.append(i.shouhin_num)
    d={"hinban_list":hinban_list,"items":items}
    return JsonResponse(d)


# 品番クリック
def hinban_click_ajax(request):
    category=request.POST.get("category")
    hinban=request.POST.get("hinban")
    if  category == "取寄せ":
        shouhin_name=Shouhin.objects.filter(shouhin_num=hinban,sample_num="").first().shouhin_name
        items=list(Shouhin.objects.filter(shouhin_num=hinban,sample_num="").values())
    else:
        shouhin_name=Shouhin.objects.filter(shouhin_num=hinban,category=category).first().shouhin_name
        items=list(Shouhin.objects.filter(shouhin_num=hinban, category=category, status=0).values())
    d={"hinban":hinban,"shouhin_name":shouhin_name,"items":items}
    return JsonResponse(d)


# 一括品名更新
def ikkatsu_hinban(request):
    hinban=request.POST["hinban_all"]
    hinmei=request.POST["hinban_all_name"]
    items=Shouhin.objects.filter(shouhin_num=hinban)
    for i in items:
        i.shouhin_name=hinmei
        i.save()
    request.session["comment"]="【一括更新】 商品番号：" + hinban + " の商品名をすべて変更しました！"
    return redirect("zaiko2:index2")


# 一括品番削除（無効）
def ikkatsu_del(request):
    hinban=request.POST["hinban_all"]
    items=Shouhin.objects.filter(shouhin_num=hinban)
    for i in items:
        i.status=1
        i.save()
    for i in items:
        if i.joutai==1:
            irai=Shouhin.objects.filter(irai_num=i.irai_num, status=0).count()
            if irai == 0:
                Rental.objects.get(irai_num_rental=i.irai_num).delete()
    request.session["comment"]="【一括削除】 商品番号：" + hinban + " のサンプルをすべて削除しました！"
    return redirect("zaiko2:index2")


# リストクリック
def list_click_ajax(request):
    hontai_num=request.POST["hontai_num"]
    item=list(Shouhin.objects.filter(hontai_num=hontai_num).values())
    d={"item":item}
    return JsonResponse(d)


# サンプル番号取得
def sample_num_auto(request):
    category=request.POST.get("category")
    if category=="":
        sample_num="no_cate"
    else:
        items=Shouhin.objects.filter(category=category) #model.pyでself.sample_numなのでサンプルNoのみ返ってくる
        if items.count() == 0:
            sample_num="no_get"
        else:
            front=str(items.first()).split("-")[0]
            back_list=[]
            for i in items:
                back_num=str(i).split("-")[1]
                back_num=back_num.replace("★","")
                back_list.append(back_num)
            back_list=list(map(int,back_list))
            for i in range(1,max(back_list)+2):
                if i not in back_list:
                    back=i
                    break
            sample_num=front + "-" + str(back)
    d={"sample_num":sample_num}
    return JsonResponse(d)


# 個別削除（無効）
def kobetsu_del(request):
    hontai_num=request.POST["h_hontai_num"]
    item=Shouhin.objects.get(hontai_num=hontai_num)
    item.status=1
    item.save()
    if item.joutai==1:
        irai=Shouhin.objects.filter(irai_num=item.irai_num, status=0).count()
        if irai == 0:
            Rental.objects.get(irai_num_rental=item.irai_num).delete()
    request.session["comment"]="【個別削除】 サンプルNo." + item.sample_num + " を削除しました！"
    return redirect("zaiko2:index2")


# 個別更新
def kobetsu_up(request):
    hontai_num=request.POST["h_hontai_num"]
    sample_num=request.POST["h_sample_num"]
    sample_num_moto=request.POST["h_sample_num_moto"]
    category=request.POST["h_category"]
    shouhin_num=request.POST["h_shouhin_num"]
    brand=request.POST["h_brand"]
    color=request.POST["h_color"]
    size=request.POST["h_size"]
    shouhin_name=request.POST["h_shouhin_name"]
    kakou=request.POST["h_kakou"]
    bikou=request.POST["h_bikou"]
    # 新規（コピーから作成）
    if hontai_num == "":
        size_num=Size.objects.get(size=size).size_num
        Shouhin.objects.create(
            sample_num=sample_num,
            category=category,
            shouhin_num=shouhin_num,
            brand=brand,
            shouhin_name=shouhin_name,
            color=color,
            size=size,
            size_num=size_num,
            kakou=kakou,
            bikou=bikou,
        )
        Label.objects.create(
            sample_num=sample_num,
            shouhin_num=shouhin_num,
            shouhin_name=shouhin_name,
            color=color,
            size=size
        )
        comment="【新規登録】 サンプルNo." + sample_num + " を登録しました！"
    # 更新
    else:
        size_num=Size.objects.get(size=size).size_num
        item=Shouhin.objects.get(hontai_num=hontai_num)
        item.sample_num=sample_num
        item.category=category
        item.shouhin_num=shouhin_num
        item.brand=brand
        item.shouhin_name=shouhin_name
        item.color=color
        item.size=size
        item.size_num=size_num
        item.kakou=kakou
        item.bikou=bikou
        item.save()
        comment="【内容更新】 サンプルNo." + sample_num + " の情報を更新しました！"

        if sample_num_moto == "": # 取り寄せ
            Label.objects.create(
                sample_num=sample_num,
                shouhin_num=shouhin_num,
                shouhin_name=shouhin_name,
                color=color,
                size=size,
            )
            comment="【新規登録】 取り寄せ商品（サンプルNo." + sample_num + "）を カテゴリ：" + category + " に登録しました！"
    request.session["comment"]=comment
    return redirect("zaiko2:index2")


# ラベル一覧に追加
def label_add(request):
    sample_num=request.POST.get("sample_num")
    item=Shouhin.objects.filter(sample_num=sample_num)
    for i in item:
        if i.status==0:
            Label.objects.create(
                sample_num=i.sample_num,
                shouhin_num=i.shouhin_num,
                shouhin_name=i.shouhin_name,
                color=i.color,
                size=i.size,
            )
            break
    d={"":""}
    return JsonResponse(d)


# ラベル一覧
def label_print(request):
    items=Label.objects.all()
    if items.count() > 16:
        items1=items[:8]
        items2=items[7:16]
        items3=items[15:]
        params={"items1":items1,"items2":items2,"items3":items3,"col":3}

    elif items.count() >8:
        items1=items[:8]
        items2=items[8:16]
        params={"items1":items1,"items2":items2,"col":2}

    else:
        items1=items[:8]
        params={"items1":items1,"col":1}

    #user認証
    kanri=0
    if request.user.username == "p1masao":
        kanri=1
    params["kanri"]=kanri

    return render(request,"zaiko2/label.html",params)


# ラベル消去
def label_del(request):
    Label.objects.all().delete()
    return redirect("zaiko2:label_print")


@login_required
def henkyaku(request):
    if "henkyaku" not in request.session:
        request.session["henkyaku"]={}
    if "msg" not in request.session["henkyaku"]:
        request.session["henkyaku"]["msg"]=""
    if "items" not in request.session["henkyaku"]:
        request.session["henkyaku"]["items"]=""

    msg=request.session["henkyaku"]["msg"]
    item_list=request.session["henkyaku"]["items"]
    items=Shouhin.objects.filter(hontai_num__in=item_list)
    #user認証
    kanri=0
    if request.user.username == "p1masao":
        kanri=1

    return render(request,"zaiko2/henkyaku.html",{"msg":msg,"items":items,"kanri":kanri})


# 返却検索
def henkyaku_kensaku(request):
    sample_num=request.POST["sample_num"]
    irai_num=request.POST["irai_num"]
    msg=""
    items=""
    if sample_num != "":
        try:
            irai_num2=Shouhin.objects.get(sample_num=sample_num).irai_num
            if irai_num2 == 0:
                msg="サンプルNo." + sample_num +  " は貸出中ではありません。"
            else:
                items=list(Shouhin.objects.filter(irai_num=irai_num2).values_list("hontai_num",flat=True))
        except:
            msg="サンプルNo." + sample_num +  " は存在しません。"
            items=""
    if irai_num != "":
        try:
            items=list(Shouhin.objects.filter(irai_num=irai_num).values_list("hontai_num",flat=True))
            irai_max=Rireki_rental.objects.all().aggregate(Max("irai_num"))
            irai_max=irai_max['irai_num__max']
            if int(irai_num) > irai_max:
                msg="依頼No." + str(irai_num) +  " は存在しません。"
            elif len(items) == 0:
                msg="依頼No." + str(irai_num) +  " はすでに返却されているか、存在しません。"
        except:
            msg="依頼No." + str(irai_num) +  " は存在しません。"

    request.session["henkyaku"]["msg"]=msg
    request.session["henkyaku"]["items"]=items
    return redirect("zaiko2:henkyaku")


# 返却リストから削除
def henkyaku_del(request):
    hen_del=request.POST.get("hen_del")
    items=request.session["henkyaku"]["items"]
    items.remove(int(hen_del))
    request.session["henkyaku"]["items"]=items
    d={"":""}
    return JsonResponse(d)


# 一括返却処理
def henkyaku_all(request):
    item_list=request.session["henkyaku"]["items"]
    today=datetime.date.today().strftime("%Y-%m-%d")
    irai_num=Shouhin.objects.get(hontai_num=item_list[0]).irai_num
    items=Shouhin.objects.filter(hontai_num__in=item_list)
    # 商品DB、貸出DB
    for i in items:
        i.joutai=0
        i.irai_num=0
        i.save()
    if Shouhin.objects.filter(irai_num=irai_num).count() == 0:
        Rental.objects.get(irai_num_rental=irai_num).delete()
    # 履歴商品DB
    ins=Rireki_shouhin.objects.filter(irai_num=irai_num)
    if ins.count() > 0:
        for i in ins:
            if i.irai_hontai_num in item_list:
                i.henkyaku=1
                i.henkyaku_day=today
                i.save()
        # 履歴DB
        if Rireki_shouhin.objects.filter(irai_num=irai_num, henkyaku=0).count() == 0:
            ins2=Rireki_rental.objects.get(irai_num=irai_num)
            ins2.status=5
            ins2.save()
    request.session["henkyaku"]["items"].clear()
    d={"":""}
    return JsonResponse(d)


# 未返却ダウンロード
def henkyaku_csv(request):
    exp_csv=[]
    a=["依頼No","依頼日","期限","所属","担当","店舗","会社","氏名","サンプルNo","商品番号","商品名","カラー","サイズ"]
    exp_csv.append(a)
    today=datetime.date.today().strftime("%Y-%m-%d")
    ins=Rireki_rental.objects.filter(status=2, rental_maxday__lt=today)
    for i in ins:
        shouhin=Rireki_shouhin.objects.filter(irai_num=i.irai_num,henkyaku=0)
        if shouhin.count() > 0:
            for h in shouhin:
                if Shouhin.objects.get(hontai_num=h.irai_hontai_num).status == 0:
                    a=[
                        i.irai_num, #依頼No
                        format(i.rental_day,"%Y-%m-%d %H:%M"), #依頼日
                        i.rental_maxday, #期限
                        i.shozoku, #所属
                        i.tantou, #担当
                        i.haisou_tempo, #店舗
                        i.haisou_com, #会社
                        i.haisou_cus, #氏名
                        Shouhin.objects.get(hontai_num=h.irai_hontai_num).sample_num, #サンプルNo
                        Shouhin.objects.get(hontai_num=h.irai_hontai_num).shouhin_num, #商品番号
                        Shouhin.objects.get(hontai_num=h.irai_hontai_num).shouhin_name, #商品名
                        Shouhin.objects.get(hontai_num=h.irai_hontai_num).color, #カラー
                        Shouhin.objects.get(hontai_num=h.irai_hontai_num).size, #サイズ
                    ]
                    exp_csv.append(a)
    now=datetime.datetime.now()
    filename=urllib.parse.quote("サンプル未返却_" + format(now,"%Y%m%d%H%M%S") +".csv")
    response = HttpResponse(content_type='text/csv; charset=CP932')
    response['Content-Disposition'] =  "attachment;  filename='{}'; filename*=UTF-8''{}".format(filename, filename)
    writer = csv.writer(response)
    for line in exp_csv:
        writer.writerow(line)
    return response


def henkyaku_spread(request):
    henkyaku_list=[]
    today=datetime.date.today().strftime("%Y-%m-%d")
    ins=Rireki_rental.objects.filter(status=2, rental_maxday__lt=today)
    for i in ins:
        shouhin=Rireki_shouhin.objects.filter(irai_num=i.irai_num,henkyaku=0)
        if shouhin.count() > 0:
            dic={
                "id":i.id, #pk
                "irai_num":i.irai_num, #依頼No
                "rental_day":format(i.rental_day,"%Y-%m-%d"), #依頼日
                "rental_maxday":i.rental_maxday, #期限
                "shozoku":i.shozoku, #所属
                "tantou":i.tantou, #担当
                "haisou_tempo":i.haisou_tempo, #店舗
                "haisou_com":i.haisou_com, #会社
                "haisou_cus":i.haisou_cus, #氏名
            }
            henkyaku_list.append(dic)

    # スプレッドシートへPOST
    url="https://script.google.com/macros/s/AKfycbxPfgge-XFGXSPg02BK7o_ZZGIusOWN-njEDw0Y_Zt7JqtoEq3ZkRNa8ME6TGiDZbLX/exec"
    henkyaku_list=json.dumps(henkyaku_list)
    requests.post(url,data=henkyaku_list)

    params={"ans":"yes"}
    #user認証
    kanri=0
    if request.user.username == "p1masao":
        kanri=1
    params["kanri"]=kanri

    return render(request,"zaiko2/henkyaku.html",params)


@login_required
def size_category(request):
    sizes=Size.objects.all().order_by("size_num")
    category=Category.objects.all().order_by("category_num")
    request.session["comment"]=""
    #user認証
    kanri=0
    if request.user.username == "p1masao":
        kanri=1
    return render(request,"zaiko2/size_category.html",{"sizes":sizes,"category":category,"kanri":kanri})


# サイズ番号（順番）
def size_num(request):
    size_list=request.POST.get("size_list")
    size_list=json.loads(size_list)
    li=[]
    for key,value in size_list.items():
        li.append(value)
    # サイズ一覧
    for size in li:
        ins=Size.objects.get(size=size)
        if ins.size_num != li.index(size)+1:
            ins.size_num=li.index(size)+1
            ins.save()
    #商品一覧
    for size in li:
        ins=Shouhin.objects.filter(size=size)
        if ins.count() != 0:
            ins2=ins[0]
            if ins2.size_num != li.index(size)+1:
                for ins2 in ins:
                    ins2.size_num=li.index(size)+1
                    ins2.save()
    d={"":""}
    return JsonResponse(d)


# サイズ名称
def size_name(request):
    old_n=request.POST.get("size_name1")
    new_n=request.POST.get("size_name2")
    # サイズ一覧
    ins=Size.objects.get(size=old_n)
    ins.size=new_n
    ins.save()
    #商品一覧
    ins=Shouhin.objects.filter(size=old_n)
    if ins.count() != 0:
        for ins2 in ins:
            ins2.size=new_n
            ins2.save()
    d={"":""}
    return JsonResponse(d)


# 新規サイズ追加
def size_new(request):
    size_new=request.POST.get("size_new")
    Size.objects.create(size_num=0, size=size_new)
    d={"":""}
    return JsonResponse(d)


# カテゴリ番号（順番）
def category_num(request):
    category_list=request.POST.get("category_list")
    category_list=json.loads(category_list)
    li=[]
    for key,value in category_list.items():
        li.append(value)
    # カテゴリ一覧
    for category in li:
        ins=Category.objects.get(category=category)
        if ins.category_num != li.index(category)+1:
            ins.category_num=li.index(category)+1
            ins.save()
    d={"":""}
    return JsonResponse(d)


# カテゴリ名称
def category_name(request):
    old_n=request.POST.get("category_name1")
    new_n=request.POST.get("category_name2")
    new_e=request.POST.get("category_name3")
    # カテゴリ一覧
    ins=Category.objects.get(category=old_n)
    ins.category=new_n
    ins.category_ex=new_e
    ins.save()
    #商品一覧
    ins=Shouhin.objects.filter(category=old_n)
    if ins.count() != 0:
        for ins2 in ins:
            ins2.category=new_n
            ins2.save()
    d={"":""}
    return JsonResponse(d)


# 新規カテゴリ追加
def category_new(request):
    category_new1=request.POST.get("category_new1")
    category_new2=request.POST.get("category_new2")
    Category.objects.create(category_num=0, category=category_new1,category_ex=category_new2)
    d={"":""}
    return JsonResponse(d)


# 登録商品CSVダウンロード
def shouhin_csv_download(request):
    ins=Shouhin.objects.all()
    exp_csv=[]
    a=["本体No","サンプルNo","カテゴリ","商品番号","ブランド","商品名","カラー","サイズ","サイズ値","加工","備考",
       "登録日","更新日","状態","依頼No","有効","最終貸出日"]
    exp_csv.append(a)
    for i in ins:
        try:
            irai_num=Rireki_shouhin.objects.filter(irai_hontai_num=i.hontai_num).aggregate(Max("irai_num"))["irai_num__max"]
            last_day=Rireki_rental.objects.get(irai_num=irai_num).rental_day.strftime("%Y-%m-%d")
        except:
            last_day=""

        a=[
            i.hontai_num, #本体No
            i.sample_num, #サンプルNo
            i.category, #カテゴリ
            i.shouhin_num, #商品番号
            i.brand, #ブランド
            i.shouhin_name, #商品名
            i.color, #カラー
            i.size, #サイズ
            i.size_num, #サイズ値
            i.kakou, #加工
            i.bikou, #備考
            i.touroku_day, #登録日
            i.koushin_day, #更新日
            i.joutai, #状態
            i.irai_num, #依頼No
            i.status, #有効
            last_day #最終貸出日
        ]
        exp_csv.append(a)
    filename=urllib.parse.quote("サンプル登録一覧.csv")
    response = HttpResponse(content_type='text/csv; charset=CP932')
    response['Content-Disposition'] =  "attachment;  filename='{}'; filename*=UTF-8''{}".format(filename, filename)
    writer = csv.writer(response)
    for line in exp_csv:
        writer.writerow(line)
    return response
