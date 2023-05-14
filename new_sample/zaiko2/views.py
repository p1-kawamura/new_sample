from django.shortcuts import render,redirect
from zaiko.models import Size,Shouhin,Category
from django.http import JsonResponse
import json


def index2(request):
    ins=Category.objects.all()
    return render(request,"zaiko2/index2.html",{"ins":ins})


# カテゴリクリック
def category_click_ajax(request):
    category=request.POST.get("category")
    if category == "取寄せ":
        items=list(Shouhin.objects.filter(sample_num = "").values())
        hinban=Shouhin.objects.filter(sample_num = "")
    else:
        items=list(Shouhin.objects.filter(category=category).values())
        hinban=Shouhin.objects.filter(category=category)
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
        shouhin_name=Shouhin.objects.filter(shouhin_num__contains=hinban,sample_num="").first().shouhin_name
        items=list(Shouhin.objects.filter(shouhin_num__contains=hinban,sample_num="").values())
    else:
        shouhin_name=Shouhin.objects.filter(shouhin_num__contains=hinban).first().shouhin_name
        items=list(Shouhin.objects.filter(shouhin_num__contains=hinban).values())
    d={"hinban":hinban,"shouhin_name":shouhin_name,"items":items}
    return JsonResponse(d)


def size_category(request):
    sizes=Size.objects.all().order_by("size_num")
    category=Category.objects.all().order_by("category_num")
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