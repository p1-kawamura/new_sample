from django.shortcuts import render,redirect
from zaiko.models import Size,Size_test,Shouhin
from django.http import JsonResponse
import json


def index2(request):
    return render(request,"zaiko2/index2.html")


def size_category(request):
    sizes=Size.objects.all().order_by("size_num")
    return render(request,"zaiko2/size_category.html",{"sizes":sizes})


# サイズ番号（順番）
def size_num(request):
    size_list=request.POST.get("size_list")
    size_list=json.loads(size_list)
    li=[]
    for key,value in size_list.items():
        li.append(value)
    print(li)
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