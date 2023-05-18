from django.shortcuts import render,redirect
from zaiko.models import Size,Shouhin,Category,Rental,Label
from django.http import JsonResponse
import json


def index2(request):
    comment=request.session["comment"]
    params={
        "ins":Category.objects.all(),
        "sizes":Size.objects.all().order_by("size_num"),
        "label":Label.objects.all().count(),
        "comment":comment
    }
    return render(request,"zaiko2/index2.html",params)


# カテゴリクリック
def category_click_ajax(request):
    category=request.POST.get("category")
    if category == "取寄せ":
        items=list(Shouhin.objects.filter(sample_num = "").values())
        hinban=Shouhin.objects.filter(sample_num = "")
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
            comment="【新規登録】 取り寄せ商品（サンプルNo." + sample_num + "）を登録しました！"
    request.session["comment"]=comment
    return redirect("zaiko2:index2")


# ラベル一覧に追加
def label_add(request):
    sample_num=request.POST.get("sample_num")
    item=Shouhin.objects.get(sample_num=sample_num)
    Label.objects.create(
                sample_num=sample_num,
                shouhin_num=item.shouhin_num,
                shouhin_name=item.shouhin_name,
                color=item.color,
                size=item.size,
            )
    d={"":""}
    return JsonResponse(d)


def size_category(request):
    sizes=Size.objects.all().order_by("size_num")
    category=Category.objects.all().order_by("category_num")
    request.session["comment"]=""
    return render(request,"zaiko2/size_category.html",{"sizes":sizes,"category":category})


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