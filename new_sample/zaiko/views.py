from django.shortcuts import render,redirect
from .models import Shouhin,Rental
import io
import csv


def index(request):
    return render(request,"zaiko/index.html")


def csv_imp_page(request):
    return render(request,"zaiko/csv_imp.html")

def dele(request):
    Shouhin.objects.all().delete()
    return render(request,"zaiko/csv_imp.html")



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