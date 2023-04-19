from django.db import models

class Shouhin(models.Model):
    hontai_num=models.AutoField("本体No",primary_key=True)
    sample_num=models.CharField("サンプルNo",max_length=20,blank=True)
    category=models.CharField("カテゴリ",max_length=10,blank=True)
    shouhin_num=models.CharField("商品番号",max_length=20,blank=True)
    brand=models.CharField("ブランド",max_length=20,blank=True)
    shouhin_name=models.CharField("商品名",max_length=255,blank=True)
    color=models.CharField("カラー",max_length=255,blank=True)
    size=models.CharField("サイズ",max_length=20,blank=True)
    size_num=models.IntegerField("サイズ値",null=True)
    kakou=models.CharField("加工",max_length=50,blank=True)
    bikou=models.CharField("備考",max_length=255,blank=True)
    touroku_day=models.DateField("登録日",null=True)
    koushin_day=models.DateField("更新日",auto_now=True)
    joutai=models.IntegerField("状態",default=0)
    irai_num=models.IntegerField("依頼No",default=0)

    def __str__(self):
        return self.sample_num
    

class Rental(models.Model):
    irai_num_rental=models.IntegerField("依頼No",null=False)
    rental_day=models.DateField("貸出日",null=True,blank=True,default="")
    busho=models.CharField("部署",max_length=30,blank=True)
    tantou=models.CharField("担当者",max_length=30,blank=True)
    com_name=models.CharField("会社名",max_length=30,blank=True)
    cus_name=models.CharField("名前",max_length=30,blank=True)
    nouhin_day=models.DateField("納品書日付",null=True,blank=True,default="")
    bikou1=models.TextField("備考1",blank=True)
    bikou2=models.TextField("備考2",blank=True)

    def __str__(self):
        return self.tantou
    

class Size(models.Model):
    size_num=models.IntegerField("順番",null=False)
    size=models.CharField("サイズ",max_length=30,blank=True)

    def __str__(self):
        return self.size

