from django.shortcuts import render,redirect
from .models import Shouhin,Rental,Size,Shozoku,Rireki_rental,Rireki_shouhin,Category
from django.contrib.auth.decorators import login_required
import io
import csv
from django.http import JsonResponse
import requests
import json
from django.db.models import Max
import datetime
from django.db.models import Q


# -----------顧客APIテスト----------
def kokyaku_index(request):
    return render(request,"zaiko/kokyaku.html")

def kokyaku_api(request):
    cus_id=request.POST["cus_id"]
    url="https://core-sys.p1-intl.co.jp/p1web/v1/customers/" + cus_id + "/receivedOrders"
    res=requests.get(url)
    res=res.json()
    res=res["receivedOrders"]


    url2="https://core-sys.p1-intl.co.jp/p1web/v1/customers/" + cus_id
    res2=requests.get(url2)
    res2=res2.json()

    return render(request,"zaiko/kokyaku.html",{"res":res,"res2":res2})

# -----------ここまで----------

@login_required
def index(request):
    if "sample" not in request.session:
        request.session["sample"]=[]
    if "hinban" not in request.session:
        request.session["hinban"]=[]
    if "color" not in request.session:
        request.session["color"]=[]
    if "size" not in request.session:
        request.session["size"]=[]
    if "page_num" not in request.session:
        request.session["page_num"]=1
    if "all_page_num" not in request.session:
        request.session["all_page_num"]=""
    if "kensaku" not in request.session:
        request.session["kensaku"]={}
    if "irai_num" not in request.session["kensaku"]:
        request.session["kensaku"]["irai_num"]=""
    if "rental_day_st" not in request.session["kensaku"]:
        request.session["kensaku"]["rental_day_st"]=""
    if "rental_day_ed" not in request.session["kensaku"]:
        request.session["kensaku"]["rental_day_ed"]=""
    if "irai_type" not in request.session["kensaku"]:
        request.session["kensaku"]["irai_type"]=""
    if "status" not in request.session["kensaku"]:
        request.session["kensaku"]["status"]=""
    if "tel" not in request.session["kensaku"]:
        request.session["kensaku"]["tel"]=""
    if "tantou" not in request.session["kensaku"]:
        request.session["kensaku"]["tantou"]=""
    if "nouhin_com" not in request.session["kensaku"]:
        request.session["kensaku"]["nouhin_com"]=""
    if "nouhin_cus" not in request.session["kensaku"]:
        request.session["kensaku"]["nouhin_cus"]=""
    if "success_num" not in request.session:
        request.session["success_num"]=""
    if "comment" not in request.session:
        request.session["comment"]=""

    request.session["comment"]="" # zaiko2:index2 の制御

    irai_shouhin_list=list(request.session["sample"])
    data=[]
    for i in irai_shouhin_list:
        data2={}
        shouhin=Shouhin.objects.get(hontai_num=i)
        data2["hontai_num"]=shouhin.hontai_num
        data2["sample_num"]=shouhin.sample_num
        data2["shouhin_num"]=shouhin.shouhin_num
        data2["color"]=shouhin.color
        data2["size"]=shouhin.size
        if shouhin.sample_num=="":
            data2["kubun"]="取り寄せ"
        else:
            data2["kubun"]="在庫"
        data.append(data2)
    kazu=len(data)
    size_list=Size.objects.all().order_by("size_num")
    shozoku_list=Shozoku.objects.all()
    today=datetime.date.today().strftime("%Y-%m-%d")
    kigen=(datetime.date.today() + datetime.timedelta(days=14)).strftime("%Y-%m-%d")
    
    #user認証
    kanri=0
    if request.user.username == "p1masao":
        kanri=1

    params={
        "irai_shouhin_list":data,
        "kazu":kazu,
        "size_list":size_list,
        "shozoku_list":shozoku_list,
        "today":today,
        "kigen":kigen,
        "kanri":kanri,
    }
    return render(request,"zaiko/index.html",params)


def shouhin_all(request):
    return render(request,"zaiko/shouhin_all.html")


@login_required
def irai_rireki(request):
    irai_num=request.session["kensaku"]["irai_num"]
    rental_day_st=request.session["kensaku"]["rental_day_st"]
    rental_day_ed=request.session["kensaku"]["rental_day_ed"]
    irai_type=request.session["kensaku"]["irai_type"]
    tantou=request.session["kensaku"]["tantou"]
    nouhin_com=request.session["kensaku"]["nouhin_com"]
    nouhin_cus=request.session["kensaku"]["nouhin_cus"]
    status=request.session["kensaku"]["status"]
    tel=request.session["kensaku"]["tel"]
    
    request.session["comment"]="" # zaiko2:index2 の制御

    #検索条件
    str={}
    if irai_num != "":
        str["irai_num"]=irai_num
    if rental_day_st != "":
        str["rental_day__gte"]=rental_day_st
    if rental_day_ed != "":
        str["rental_day__lte"]=rental_day_ed
    if irai_type != "":
        str["irai_type"]=irai_type
    if tantou != "":
        str["tantou__contains"]=tantou
    if nouhin_com != "":
        str["nouhin_com__contains"]=nouhin_com
    if nouhin_cus != "":
        str["nouhin_cus__contains"]=nouhin_cus
    if status != "":
        str["status"]=status
    if tel != "":
        str["haisou_tel_kensaku"]=tel.replace("-","")
        

    items=Rireki_rental.objects.filter(**str).order_by("irai_num").reverse()
    shozoku_list=Shozoku.objects.all()
    #全ページ数
    if items.count()==0:
        all_num=1
    elif items.count() % 30== 0:
        all_num=items.count() / 30
    else:
        all_num=items.count() // 30 + 1
    all_num=int(all_num)
    request.session["all_page_num"]=all_num
    num=request.session["page_num"]
    items=items[(num-1)*30 : num*30]

    #user認証
    kanri=0
    if request.user.username == "p1masao":
        kanri=1

    params={
        "items":items,
        "shozoku_list":shozoku_list,
        "num":num,
        "all_num":all_num,
        "kanri":kanri,
    }
    return render(request,"zaiko/rireki.html",params)


def rireki_kensaku(request):
    irai_num=request.POST["irai_num"]
    rental_day_st=request.POST["rental_day_st"]
    rental_day_ed=request.POST["rental_day_ed"]
    irai_type=request.POST["irai_type"]
    tantou=request.POST["tantou"]
    nouhin_com=request.POST["nouhin_com"]
    nouhin_cus=request.POST["nouhin_cus"]
    status=request.POST["status"]
    tel=request.POST["tel"]

    request.session["kensaku"]["irai_num"]=irai_num
    request.session["kensaku"]["rental_day_st"]=rental_day_st
    request.session["kensaku"]["rental_day_ed"]=rental_day_ed
    request.session["kensaku"]["irai_type"]=irai_type
    request.session["kensaku"]["tantou"]=tantou
    request.session["kensaku"]["nouhin_com"]=nouhin_com
    request.session["kensaku"]["nouhin_cus"]=nouhin_cus
    request.session["kensaku"]["status"]=status
    request.session["kensaku"]["tel"]=tel
    request.session["page_num"]=1

    return redirect("zaiko:irai_rireki")


def rireki_kensaku_all(request):
    request.session["kensaku"]["irai_num"]=""
    request.session["kensaku"]["rental_day_st"]=""
    request.session["kensaku"]["rental_day_ed"]=""
    request.session["kensaku"]["irai_type"]=""
    request.session["kensaku"]["tantou"]=""
    request.session["kensaku"]["nouhin_com"]=""
    request.session["kensaku"]["nouhin_cus"]=""
    request.session["kensaku"]["status"]=""
    request.session["kensaku"]["tel"]=""
    request.session["page_num"]=1
    return redirect("zaiko:irai_rireki")


def page_prev(request):
    num=request.session["page_num"]
    if num-1 > 0:
        request.session["page_num"] = num - 1
    return redirect("zaiko:irai_rireki")


def page_first(request):
    request.session["page_num"] = 1
    return redirect("zaiko:irai_rireki")


def page_next(request):
    num=request.session["page_num"]
    all_num=request.session["all_page_num"]
    if num+1 <= all_num:
        request.session["page_num"] = num + 1
    return redirect("zaiko:irai_rireki")


def page_last(request):
    all_num=request.session["all_page_num"]
    request.session["page_num"]=all_num
    return redirect("zaiko:irai_rireki")


def csv_imp_page(request):
    return render(request,"zaiko/csv_imp.html")


def dele(request):
    Shouhin.objects.all().delete()
    return render(request,"zaiko/csv_imp.html")


#品番検索に入力
def hinban_enter_ajax(request):
    hinban=request.POST.get("hinban")
    if len(hinban)==0:
        shouhin_list=[]
    else:
        items=Shouhin.objects.filter(~Q(sample_num=""),shouhin_num__contains = hinban ,status=0)
        shouhin_list=[]
        for item in items:
            if item.shouhin_num not in shouhin_list:
                shouhin_list.append(item.shouhin_num)
        shouhin_list.sort()
    d={"hinban":shouhin_list}
    return JsonResponse(d)


#品番リストをクリック（リストボックス）
def hinban_click_ajax(request):
    hinban=request.POST.get("hinban")
    request.session["hinban"]=hinban
    items=Shouhin.objects.filter(~Q(sample_num=""),shouhin_num = hinban,status=0).order_by("size_num")
    color_list=[]
    size_list=[]
    for item in items:
        shouhin_name=item.shouhin_name
        brand=item.brand
        if item.color not in color_list:
            color_list.append(item.color)
        if item.size not in size_list:
            size_list.append(item.size)
    color_list.sort()
    d={
        "color":color_list,
        "size":size_list,
        "shouhin_name":shouhin_name,
        "brand":brand,
    }
    return JsonResponse(d)


#品番リストをクリック（商品一覧）
def hinban_click_ajax2(request):
    hinban=request.session["hinban"]
    items=list(Shouhin.objects.filter(~Q(sample_num=""),shouhin_num = hinban,status=0).order_by("color","size_num").values())
    items2=list(Rental.objects.all().values())
    data={
        "items":items,
        "items2":items2,
     }
    return render(request,"zaiko/shouhin_all.html",data)


#カラー、サイズをクリック
def color_size_click_ajax(request):
    color=request.POST.get("color")
    size=request.POST.get("size") 
    request.session["color"]=color
    request.session["size"]=size
    d={"":""}
    return JsonResponse(d)


#カラー、サイズをクリック（商品一覧）
def color_size_click_ajax2(request):
    hinban=request.session["hinban"]
    color=request.session["color"]
    size=request.session["size"]
    try:
        color=color.split(",")
    except:
        color=list(color)
    try:
        size=size.split(",")
    except:
        size=list(size)

    #商品一覧
    if color[0]=="" and size[0]=="":
        items=list(Shouhin.objects.filter(~Q(sample_num=""),shouhin_num = hinban, status=0).order_by("color","size_num").values())
    elif color[0]!="" and size[0]=="" :
        items=list(Shouhin.objects.filter(~Q(sample_num=""),shouhin_num = hinban , color__in=color, status=0).order_by("color","size_num").values())
    elif color[0]=="" and size[0]!="" :
        items=list(Shouhin.objects.filter(~Q(sample_num=""),shouhin_num = hinban , size__in=size, status=0).order_by("color","size_num").values())
    else:
        items=list(Shouhin.objects.filter(~Q(sample_num=""),shouhin_num = hinban , color__in=color , size__in=size, status=0).order_by("color","size_num").values())
    items2=list(Rental.objects.all().values())
    data={
        "items": items,
        "items2": items2,
        }
    return render(request,"zaiko/shouhin_all.html",data)


#加工方法ボタンをクリック
def kakou_click_ajax(request):
    items=Shouhin.objects.filter(category = "加工" , status=0)
    shouhin_list=[]
    for item in items:
        if item.shouhin_num not in shouhin_list:
            shouhin_list.append(item.shouhin_num)
    shouhin_list.sort()
    d={"hinban":shouhin_list}
    return JsonResponse(d)


#スワッチボタンをクリック
def swatch_click_ajax(request):
    items=Shouhin.objects.filter(category = "SW" , status=0)
    shouhin_list=[]
    for item in items:
        if item.shouhin_num not in shouhin_list:
            shouhin_list.append(item.shouhin_num)
    shouhin_list.sort()
    d={"hinban":shouhin_list}
    return JsonResponse(d)


#キープの解除
def keep_kaijo_ajax(request):
    keep_hontai_num=request.POST.get("hontai_num")
    keep_irai_num=request.POST.get("irai_num")
    shouhin=Shouhin.objects.get(hontai_num=keep_hontai_num)
    shouhin.joutai=0
    shouhin.irai_num=0
    shouhin.save()
    if Shouhin.objects.filter(irai_num=keep_irai_num).count()==0:
        Rental.objects.get(irai_num_rental=keep_irai_num).delete()
    d={"":""}
    return JsonResponse(d)


# 依頼商品チェック動作
def check_addlist_ajax(request):
    ans=request.POST.get("ans")
    hontai_num=request.POST.get("hontai_num")
    ses=list(request.session["sample"])
    if ans == "yes":
        if hontai_num not in ses:
            ses.append(hontai_num)
    else:
        ses.remove(hontai_num)
    request.session["sample"]=ses
    d={"":""}
    return JsonResponse(d)


#取寄せ商品追加ボタン（モーダル）
def toriyose_add_ajax(request):
    data=request.POST.get("rows")
    data=json.loads(data)
    ses=list(request.session["sample"])
    for i in range(1,6):
        li=data[i]
        if li[0]!="":
            try:
                size_num=Size.objects.get(size=li[5]).size_num
            except:
                size_num=0
            Shouhin.objects.create(shouhin_num=li[0], brand=li[1], shouhin_name=li[2], color=li[3], size=li[5], size_num=size_num)
            hontai=Shouhin.objects.all().aggregate(Max("hontai_num"))
            ses.append(str(hontai['hontai_num__max']))
    request.session["sample"]=ses 
    d={"":""}
    return JsonResponse(d)


# 依頼商品から削除
def irai_del_ajax(request):
    del_num=request.POST.get("irai_del")
    ses=list(request.session["sample"])
    shouhin=Shouhin.objects.get(hontai_num=del_num)
    if shouhin.sample_num == "":
        shouhin.delete()
    ses.remove(del_num)
    request.session["sample"]=ses
    d={"":""}
    return JsonResponse(d)


#依頼前最終確認
def last_kakunin(request):
    ses=list(request.session["sample"])
    data=[]
    for i in ses:
        joutai=Shouhin.objects.get(hontai_num=i).joutai
        if joutai !=0:
            data.append(i)
    d={"data":data}
    return JsonResponse(d)


# 依頼確定（顧客　貸出：1　履歴内容：0）
def haisou_cus_success(request):
    shozoku=request.POST["c_shozoku"]
    tantou=request.POST["c_tantou"]
    bikou2=request.POST["c_bikou2"]
    haisou_deliday=request.POST["c_haisou_deliday"]
    haisou_com=request.POST["c_haisou_com"]
    haisou_cus=request.POST["c_haisou_cus"]
    haisou_yubin=request.POST["c_haisou_yubin"]
    haisou_pref=request.POST["c_haisou_pref"]
    haisou_city=request.POST["c_haisou_city"]
    haisou_banchi=request.POST["c_haisou_banchi"]
    haisou_build=request.POST["c_haisou_build"]
    haisou_tel=request.POST["c_haisou_tel"]
    haisou_mail=request.POST["c_haisou_mail"]
    haisou_com_m=request.POST["c_haisou_com_m"]
    haisou_cus_m=request.POST["c_haisou_cus_m"]
    haisou_yubin_m=request.POST["c_haisou_yubin_m"]
    haisou_pref_m=request.POST["c_haisou_pref_m"]
    haisou_city_m=request.POST["c_haisou_city_m"]
    haisou_banchi_m=request.POST["c_haisou_banchi_m"]
    haisou_build_m=request.POST["c_haisou_build_m"]
    haisou_tel_m=request.POST["c_haisou_tel_m"]
    nouhin_com=request.POST["c_nouhin_com"]
    nouhin_cus=request.POST["c_nouhin_cus"]
    nouhin_day=request.POST["c_nouhin_day"]
    rental_maxday=request.POST["c_rental_maxday"]
    bikou1=request.POST["c_bikou1"]
    ses=list(request.session["sample"])
    irai_num=Rireki_rental.objects.all().aggregate(Max("irai_num"))
    irai_num=irai_num['irai_num__max'] + 1
    for i in ses:
        # 商品DB
        item=Shouhin.objects.get(hontai_num=i)
        item.joutai=1
        item.irai_num=irai_num
        item.save()
        # 商品履歴DB
        if item.sample_num=="":
            kubun="取り寄せ"
        else:
            kubun="在庫"
        Rireki_shouhin.objects.create(irai_num=irai_num,irai_hontai_num=i,irai_hontai_kubun=kubun)

    #貸出DB
    Rental.objects.create(
        irai_num_rental = irai_num,
        busho = shozoku,
        tantou = tantou,
        com_name = nouhin_com,
        cus_name = nouhin_cus,
    )
    #貸出履歴DB
    Rireki_rental.objects.create(
        irai_num = irai_num,
        irai_type = 0,
        shozoku = shozoku,
        tantou = tantou,
        haisou_deliday = haisou_deliday,
        haisou_com = haisou_com,
        haisou_cus = haisou_cus,
        haisou_yubin = haisou_yubin,
        haisou_pref = haisou_pref,
        haisou_city = haisou_city,
        haisou_banchi = haisou_banchi,
        haisou_build = haisou_build,
        haisou_tel = haisou_tel,
        haisou_tel_kensaku = haisou_tel.replace("-","").strip(),
        haisou_mail = haisou_mail,
        haisou_com_m = haisou_com_m,
        haisou_cus_m = haisou_cus_m,
        haisou_yubin_m = haisou_yubin_m,
        haisou_pref_m = haisou_pref_m,
        haisou_city_m = haisou_city_m,
        haisou_banchi_m = haisou_banchi_m,
        haisou_build_m = haisou_build_m,
        haisou_tel_m = haisou_tel_m,
        nouhin_com = nouhin_com,
        nouhin_cus = nouhin_cus,
        nouhin_day = nouhin_day,
        rental_maxday = rental_maxday,
        bikou1 = bikou1,
        bikou2 = bikou2,
    )
    request.session["sample"].clear()
    request.session["success_num"]=irai_num
    return redirect("zaiko:irai_success")


# 依頼確定（店舗　貸出：1　履歴内容：1）
def haisou_tempo_success(request):
    shozoku=request.POST["t_shozoku"]
    tantou=request.POST["t_tantou"]
    haisou_tempo=request.POST["t_haisou_tempo"]
    bikou2=request.POST["t_bikou2"]
    nouhin_com=request.POST["t_nouhin_com"]
    nouhin_cus=request.POST["t_nouhin_cus"]
    nouhin_day=request.POST["t_nouhin_day"]
    rental_maxday=request.POST["t_rental_maxday"]
    bikou1=request.POST["t_bikou1"]
    ses=list(request.session["sample"])
    irai_num=Rireki_rental.objects.all().aggregate(Max("irai_num"))
    irai_num=irai_num['irai_num__max'] + 1
    for i in ses:
        # 商品DB
        item=Shouhin.objects.get(hontai_num=i)
        item.joutai=1
        item.irai_num=irai_num
        item.save()
        # 商品履歴DB
        if item.sample_num=="":
            kubun="取り寄せ"
        else:
            kubun="在庫"
        Rireki_shouhin.objects.create(irai_num=irai_num,irai_hontai_num=i,irai_hontai_kubun=kubun)

    #貸出DB
    Rental.objects.create(
        irai_num_rental = irai_num,
        busho = shozoku,
        tantou = tantou,
        com_name = nouhin_com,
        cus_name = nouhin_cus,
    )
    #貸出履歴DB
    Rireki_rental.objects.create(
        irai_num = irai_num,
        irai_type = 1,
        shozoku = shozoku,
        tantou = tantou,
        haisou_tempo = haisou_tempo,
        nouhin_com = nouhin_com,
        nouhin_cus = nouhin_cus,
        nouhin_day = nouhin_day,
        rental_maxday = rental_maxday,
        bikou1 = bikou1,
        bikou2 = bikou2,
    )
    request.session["sample"].clear()
    request.session["success_num"]=irai_num
    return redirect("zaiko:irai_success")


# 依頼確定（キープ　貸出：1　履歴内容：2）
def haisou_keep_success(request):
    shozoku=request.POST["k_shozoku"]
    tantou=request.POST["k_tantou"]
    bikou2=request.POST["k_bikou2"]
    nouhin_com=request.POST["k_nouhin_com"]
    nouhin_cus=request.POST["k_nouhin_cus"]
    ses=list(request.session["sample"])
    irai_num=Rireki_rental.objects.all().aggregate(Max("irai_num"))
    irai_num=irai_num['irai_num__max'] + 1
    for i in ses:
        # 商品DB
        item=Shouhin.objects.get(hontai_num=i)
        item.joutai=2
        item.irai_num=irai_num
        item.save()
        # 商品履歴DB
        if item.sample_num=="":
            kubun="取り寄せ"
        else:
            kubun="在庫"
        Rireki_shouhin.objects.create(irai_num=irai_num,irai_hontai_num=i,irai_hontai_kubun=kubun)

    #貸出DB
    Rental.objects.create(
        irai_num_rental = irai_num,
        busho = shozoku,
        tantou = tantou,
        com_name = nouhin_com,
        cus_name = nouhin_cus,
        status = 4,
    )
    #貸出履歴DB
    Rireki_rental.objects.create(
        irai_num = irai_num,
        irai_type = 2,
        shozoku = shozoku,
        tantou = tantou,
        nouhin_com = nouhin_com,
        nouhin_cus = nouhin_cus,
        bikou2 = bikou2,
    )
    request.session["sample"].clear()
    request.session["success_num"]=irai_num
    return redirect("zaiko:irai_success")


# 依頼確定表示
def irai_success(request):
    success_num=request.session["success_num"]
    irai_detail=Rireki_rental.objects.get(irai_num=success_num)
    irai_num=success_num
    items=Rireki_shouhin.objects.filter(irai_num=irai_num).values_list("irai_hontai_num",flat=True)
    irai_shouhin_list=list(items)
    data=[]
    for i in irai_shouhin_list:
        data2={}
        shouhin=Shouhin.objects.get(hontai_num=i)
        data2["hontai_num"]=shouhin.hontai_num
        data2["sample_num"]=shouhin.sample_num
        data2["shouhin_num"]=shouhin.shouhin_num
        data2["color"]=shouhin.color
        data2["size"]=shouhin.size
        data2["kubun"]=Rireki_shouhin.objects.get(irai_num=irai_num,irai_hontai_num=i).irai_hontai_kubun
        data.append(data2)
    params={
            "irai_shouhin_list":data,
            "irai_detail":irai_detail,
            "kubun":"new",
        }
    return render(request,"zaiko/success.html",params)


# 履歴確認ボタン
def rireki_kakunin(request,pk):
    irai_detail=Rireki_rental.objects.get(pk=pk)
    irai_type=irai_detail.irai_type
    status=irai_detail.status
    if status==0: #success.htmlのタイトル用
        kubun="kakunin_ok"
    elif status==1:
        kubun="junbi"
    else:
        kubun="kakunin_no"
    irai_num=irai_detail.irai_num
    items=Rireki_shouhin.objects.filter(irai_num=irai_num).values_list("irai_hontai_num",flat=True)
    irai_shouhin_list=list(items)
    data=[]
    for i in irai_shouhin_list:
        data2={}
        shouhin=Shouhin.objects.get(hontai_num=i)
        data2["hontai_num"]=shouhin.hontai_num
        data2["sample_num"]=shouhin.sample_num
        data2["shouhin_num"]=shouhin.shouhin_num
        data2["color"]=shouhin.color
        data2["size"]=shouhin.size
        data2["kubun"]=Rireki_shouhin.objects.get(irai_num=irai_num,irai_hontai_num=i).irai_hontai_kubun
        data.append(data2)
    params={
            "irai_shouhin_list":data,
            "irai_detail":irai_detail,
            "kubun":kubun,
        }
    return render(request,"zaiko/success.html",params)


# キャンセル依頼
def cancel_ajax(request):
    irai_num=request.POST.get("irai_num")
    name=request.POST.get("name")
    today=datetime.date.today().strftime("%Y-%m-%d")
    # 貸出一覧
    Rental.objects.get(irai_num_rental=irai_num).delete()
    # 商品一覧
    can=Shouhin.objects.filter(irai_num=irai_num)
    for i in can:
        i.joutai=0
        i.irai_num=0
        i.save()
    # 履歴　貸出一覧
    can=Rireki_rental.objects.get(irai_num=irai_num)
    can.status=3
    can.cancel_day=today
    can.cancel_name=name
    can.save()
    d={"":""}
    return JsonResponse(d)



# 元DB取込
def csv_imp(request):

    # #在庫リスト
    # data = io.TextIOWrapper(request.FILES['csv1'].file, encoding="cp932")
    # csv_content = csv.reader(data)
    
    # csv_list=list(csv_content)
        
    # h=0
    # for i in csv_list:
    #     if h!=0:
    #         Shouhin.objects.update_or_create(
    #             sample_num=i[1],
    #             defaults={
    #                 "sample_num":i[1],
    #                 "category":i[2],
    #                 "shouhin_num":i[3],
    #                 "brand":i[4],
    #                 "shouhin_name":i[5],
    #                 "color":i[6],
    #                 "size":i[7],
    #                 "size_num":i[8],
    #                 "kakou":i[9],
    #                 "bikou":i[10],
    #                 "joutai":i[13],
    #                 "irai_num":i[14],
    #             }            
    #         )
    #     h+=1


    # #貸出リスト
    # data = io.TextIOWrapper(request.FILES['csv2'].file, encoding="cp932")
    # csv_content = csv.reader(data)
    
    # csv_list=list(csv_content)
        
    # h=0
    # for i in csv_list:
    #     if h!=0:
    #         Rental.objects.update_or_create(
    #             irai_num_rental=i[0],
    #             defaults={
    #                 "irai_num_rental":i[0],
    #                 "rental_day":i[1],
    #                 "busho":i[2],
    #                 "tantou":i[3],
    #                 "com_name":i[4],
    #                 "cus_name":i[5],
    #                 "nouhin_day":i[6],
    #                 "bikou1":i[7],
    #                 "bikou2":i[8],
    #             }            
    #         )
    #     h+=1

    
    # #サイズリスト
    # data = io.TextIOWrapper(request.FILES['csv3'].file, encoding="cp932")
    # csv_content = csv.reader(data)
    
    # csv_list=list(csv_content)
        
    # h=0
    # for i in csv_list:
    #     if h!=0:
    #         Size.objects.update_or_create(
    #             size_num=i[0],
    #             defaults={
    #                 "size_num":i[0],
    #                 "size":i[1],
    #             }            
    #         )
    #     h+=1


    #カテゴリリスト
    data = io.TextIOWrapper(request.FILES['csv4'].file, encoding="cp932")
    csv_content = csv.reader(data)
    
    csv_list=list(csv_content)
        
    h=0
    for i in csv_list:
        if h!=0:
            Category.objects.update_or_create(
                category_num=i[0],
                defaults={
                    "category_num":i[0],
                    "category":i[1],
                    "category_ex":i[2],
                }            
            )
        h+=1  

    return render(request,"zaiko/csv_imp.html",{"message":"CSVの読み込みが完了しました"})
