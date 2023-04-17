from django.shortcuts import render,redirect
from .models import Shouhin,Rental
import io
import csv
from django.http import JsonResponse
import requests


# 顧客APIテスト
def index2(request):
    return render(request,"zaiko/kokyaku.html")

def test(request):
    cus_id=request.POST["cus_id"]
    url="https://core-sys.p1-intl.co.jp/p1web/v1/customers/" + cus_id + "/receivedOrders"
    res=requests.get(url)
    res=res.json()
    res=res["receivedOrders"]


    url2="https://core-sys.p1-intl.co.jp/p1web/v1/customers/" + cus_id
    res2=requests.get(url2)
    res2=res2.json()

    return render(request,"zaiko/kokyaku.html",{"res":res,"res2":res2})


# ---------ここまで　顧客APIテスト--------------
def index(request):
    if "sample" not in request.session:
        request.session["sample"]=[]
    irai_shouhin_list=list(request.session["sample"])
    data=[]
    print(irai_shouhin_list)
    for i in irai_shouhin_list:
        if i=="":
            irai_shouhin_list.remove("")
    print(irai_shouhin_list)
    request.session["sample"]=irai_shouhin_list
    for i in irai_shouhin_list:
        shouhin=Shouhin.objects.get(hontai_num=i)
        data2={}
        data2["hontai_num"]=shouhin.hontai_num
        data2["sample_num"]=shouhin.sample_num
        data2["shouhin_num"]=shouhin.shouhin_num
        data2["brand"]=shouhin.brand
        data2["shouhin_name"]=shouhin.shouhin_name
        data2["color"]=shouhin.color
        data2["size"]=shouhin.size
        data2["kubun"]="在庫"
        data.append(data2)
    if len(data)==0:
        hyouji="no"
    else:
        hyouji="yes"
    return render(request,"zaiko/index.html",{"irai_shouhin_list":data,"hyouji":hyouji})


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


#品番リストをクリック
def hinban_click_ajax(request):
    hinban=request.POST.get("hinban")
    items=Shouhin.objects.filter(shouhin_num = hinban).order_by("size_num")
    items2=list(Shouhin.objects.filter(shouhin_num = hinban).order_by("color","size_num").values())
    items3=list(Rental.objects.all().values())
    color_list=[]
    size_list=[]
    for item in items:
        hinmei=item.shouhin_name
        brand=item.brand
        if item.color not in color_list:
            color_list.append(item.color)
        if item.size not in size_list:
            size_list.append(item.size)
    color_list.sort()
    shouhin_name=hinban + "　" + hinmei
    d={
        "color":color_list,
        "size":size_list,
        "items":items2,
        "items3":items3,
        "shouhin_name":shouhin_name,
        "brand":brand
     }
    return JsonResponse(d)


#カラー、サイズをクリック
def color_size_click_ajax(request):
    hinban=request.POST.get("hinban")
    color=request.POST.get("color")
    size=request.POST.get("size")
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
    items3=list(Rental.objects.all().values())
    d={
        "items": items,
        "items3": items3
        }          
    return JsonResponse(d)


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


# 依頼商品から削除
def irai_del_ajax(request):
    del_num=request.POST.get("irai_del")
    ses=list(request.session["sample"])
    ses.remove(del_num)
    request.session["sample"]=ses
    d={"":""}
    return JsonResponse(d)


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

    return render(request,"zaiko/csv_imp.html",{"message":"CSVの読み込みが完了しました"})