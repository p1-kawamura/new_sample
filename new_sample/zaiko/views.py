from django.shortcuts import render,redirect
from .models import Shouhin,Rental,Size,Shozoku
import io
import csv
from django.http import JsonResponse
import requests
import json
from django.db.models import Max
import datetime



# 顧客APIテスト
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


def index(request):
    if "sample" not in request.session:
        request.session["sample"]=[]
    if "hinban" not in request.session:
        request.session["hinban"]=[]
    if "color" not in request.session:
        request.session["color"]=[]
    if "size" not in request.session:
        request.session["size"]=[]
    if "shouhin_name" not in request.session:
        request.session["size"]=[]
    if "brand" not in request.session:
        request.session["brand"]=[]

    irai_shouhin_list=list(request.session["sample"])
    data=[]
    for i in irai_shouhin_list:
        data2={}
        shouhin=Shouhin.objects.get(hontai_num=i)
        data2["hontai_num"]=shouhin.hontai_num
        data2["sample_num"]=shouhin.sample_num
        data2["shouhin_num"]=shouhin.shouhin_num
        data2["brand"]=shouhin.brand
        data2["shouhin_name"]=shouhin.shouhin_name
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
    params={
        "irai_shouhin_list":data,
        "kazu":kazu,
        "size_list":size_list,
        "shozoku_list":shozoku_list,
        "today":today,
        "kigen":kigen
    }
    return render(request,"zaiko/index.html",params)


def shouhin_all(request):
    return render(request,"zaiko/shouhin_all.html",{"shouhin_hyouji":"no"})


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
        items=Shouhin.objects.filter(shouhin_num__contains = hinban)
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
    items=Shouhin.objects.filter(shouhin_num = hinban).order_by("size_num")
    color_list=[]
    size_list=[]
    for item in items:
        if item.color not in color_list:
            color_list.append(item.color)
        if item.size not in size_list:
            size_list.append(item.size)
    color_list.sort()
    d={
        "color":color_list,
        "size":size_list,
     }
    return JsonResponse(d)


#品番リストをクリック（商品一覧）
def hinban_click_ajax2(request):
    hinban=request.session["hinban"]
    items=list(Shouhin.objects.filter(shouhin_num = hinban).order_by("color","size_num").values())
    items2=list(Rental.objects.all().values())
    shouhin_name=hinban + "　" + items[0]["shouhin_name"]
    brand=items[0]["brand"]  
    request.session["shouhin_name"]=shouhin_name
    request.session["brand"]=brand
    data={
        "items":items,
        "items2":items2,
        "shouhin_name":shouhin_name,
        "brand":brand
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
    shouhin_name=request.session["shouhin_name"]
    brand=request.session["brand"]
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
        items=list(Shouhin.objects.filter(shouhin_num = hinban).order_by("color","size_num").values())
    elif color[0]!="" and size[0]=="" :
        items=list(Shouhin.objects.filter(shouhin_num = hinban , color__in=color).order_by("color","size_num").values())
    elif color[0]=="" and size[0]!="" :
        items=list(Shouhin.objects.filter(shouhin_num = hinban , size__in=size).order_by("color","size_num").values())
    else:
        items=list(Shouhin.objects.filter(shouhin_num = hinban , color__in=color , size__in=size).order_by("color","size_num").values())
    items2=list(Rental.objects.all().values())
    data={
        "items": items,
        "items2": items2,
        "shouhin_name":shouhin_name,
        "brand":brand
        }
    return render(request,"zaiko/shouhin_all.html",data)


#加工方法ボタンをクリック
def kakou_click_ajax(request):
    items=Shouhin.objects.filter(category = "加工")
    shouhin_list=[]
    for item in items:
        if item.shouhin_num not in shouhin_list:
            shouhin_list.append(item.shouhin_num)
    shouhin_list.sort()
    d={"hinban":shouhin_list}
    return JsonResponse(d)


#スワッチボタンをクリック
def swatch_click_ajax(request):
    items=Shouhin.objects.filter(category = "SW")
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


#依頼商品追加ボタン
def check_addlist_ajax(request):
    check_addlist=request.POST.get("check_addlist")
    try:
        check_addlist=check_addlist.split(",")
    except:
        check_addlist=list(check_addlist)
    ses=list(request.session["sample"])
    for i in check_addlist:
        if i not in ses:
            ses.append(i)
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


# 配送先（顧客）
def haisou_cus(request):
    shozoku=request.POST["c_shozoku"]
    tantou=request.POST["c_tantou"]
    print(shozoku,tantou)
    return redirect("zaiko:index")


# 元DB取込
def csv_imp(request):

    #在庫リスト
    data = io.TextIOWrapper(request.FILES['csv1'].file, encoding="cp932")
    csv_content = csv.reader(data)
    
    csv_list=list(csv_content)
        
    h=0
    for i in csv_list:
        if h!=0:
            Shouhin.objects.update_or_create(
                sample_num=i[1],
                defaults={
                    "sample_num":i[1],
                    "category":i[2],
                    "shouhin_num":i[3],
                    "brand":i[4],
                    "shouhin_name":i[5],
                    "color":i[6],
                    "size":i[7],
                    "size_num":i[8],
                    "kakou":i[9],
                    "bikou":i[10],
                    "joutai":i[13],
                    "irai_num":i[14],
                }            
            )
        h+=1


    #貸出リスト
    data = io.TextIOWrapper(request.FILES['csv2'].file, encoding="cp932")
    csv_content = csv.reader(data)
    
    csv_list=list(csv_content)
        
    h=0
    for i in csv_list:
        if h!=0:
            Rental.objects.update_or_create(
                irai_num_rental=i[0],
                defaults={
                    "irai_num_rental":i[0],
                    "rental_day":i[1],
                    "busho":i[2],
                    "tantou":i[3],
                    "com_name":i[4],
                    "cus_name":i[5],
                    "nouhin_day":i[6],
                    "bikou1":i[7],
                    "bikou2":i[8],
                }            
            )
        h+=1

    
    #サイズリスト
    data = io.TextIOWrapper(request.FILES['csv3'].file, encoding="cp932")
    csv_content = csv.reader(data)
    
    csv_list=list(csv_content)
        
    h=0
    for i in csv_list:
        if h!=0:
            Size.objects.update_or_create(
                size_num=i[0],
                defaults={
                    "size_num":i[0],
                    "size":i[1],
                }            
            )
        h+=1  

    return render(request,"zaiko/csv_imp.html",{"message":"CSVの読み込みが完了しました"})