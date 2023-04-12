from django.shortcuts import render,redirect
from .models import Shouhin,Rental
import io
import csv
from django.http import JsonResponse


def index(request):
    return render(request,"zaiko/index.html")


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
        "items":items2,
     }
    return JsonResponse(d)


#カラーをクリック
def color_click_ajax(request):
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
    d={"items": items}          
    return JsonResponse(d)





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