from django.shortcuts import render
from zaiko.models import Size_test

def index2(request):
    return render(request,"zaiko2/index2.html")


def size_category(request):
    sizes=Size_test.objects.all().order_by("size_num")
    return render(request,"zaiko2/size_category.html",{"sizes":sizes})
