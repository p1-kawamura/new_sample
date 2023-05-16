from django.db import models

class Shouhin(models.Model):
    hontai_num=models.AutoField("本体No",primary_key=True)
    sample_num=models.CharField("サンプルNo",max_length=20,blank=True)
    category=models.CharField("カテゴリ",max_length=50,blank=True)
    shouhin_num=models.CharField("商品番号",max_length=20,blank=True)
    brand=models.CharField("ブランド",max_length=20,blank=True)
    shouhin_name=models.CharField("商品名",max_length=255,blank=True)
    color=models.CharField("カラー",max_length=255,blank=True)
    size=models.CharField("サイズ",max_length=20,blank=True)
    size_num=models.IntegerField("サイズ値",default=0)
    kakou=models.CharField("加工",max_length=50,blank=True)
    bikou=models.CharField("備考",max_length=255,blank=True)
    touroku_day=models.DateField("登録日",auto_now_add=True)
    koushin_day=models.DateField("更新日",auto_now=True)
    joutai=models.IntegerField("状態",default=0)
    irai_num=models.IntegerField("依頼No",default=0)
    status=models.IntegerField("有効",default=0)

    def __str__(self):
        return self.sample_num
    
    # joutai（状態）　0:在庫有り　1:貸出中　2:キープ中
    # status（有効）　0:有効　1:無効
    

class Rental(models.Model):
    irai_num_rental=models.IntegerField("依頼No",null=False)
    rental_day=models.DateField("貸出日",auto_now_add=True)
    busho=models.CharField("所属",max_length=30,blank=True)
    tantou=models.CharField("担当者",max_length=30,blank=True)
    com_name=models.CharField("会社名",max_length=30,blank=True)
    cus_name=models.CharField("名前",max_length=30,blank=True)

    def __str__(self):
        return self.tantou
    
    # com_name、cus_nameは納品書の会社、氏名（Rireki_rentalのnouhin_com、nouhin_cus）
    

class Size(models.Model):
    size_num=models.IntegerField("順番",null=False)
    size=models.CharField("サイズ",max_length=30,blank=True)

    def __str__(self):
        return self.size
    

class Category(models.Model):
    category_num=models.IntegerField("順番",null=False)
    category=models.CharField("カテゴリ",max_length=50,blank=True)
    category_ex=models.CharField("説明",max_length=100,blank=True)

    def __str__(self):
        return self.category
    

class Shozoku(models.Model):
    shozoku=models.CharField("所属",max_length=30)

    def __str__(self):
        return self.shozoku


class Rireki_rental(models.Model):
    irai_num=models.IntegerField("依頼No",null=False)
    irai_type=models.IntegerField("内容")
    rental_day=models.DateField("貸出日",auto_now_add=True)
    shozoku=models.CharField("所属",max_length=30,blank=True)
    tantou=models.CharField("担当者",max_length=30,blank=True)
    haisou_tempo=models.CharField("配送店舗",max_length=30,blank=True)
    haisou_com=models.CharField("会社名",max_length=30,blank=True)
    haisou_cus=models.CharField("名前",max_length=30,blank=True)
    haisou_yubin=models.CharField("郵便番号",max_length=30,blank=True)
    haisou_pref=models.CharField("都道府県",max_length=10,blank=True)
    haisou_city=models.CharField("市区町村",max_length=30,blank=True)
    haisou_banchi=models.CharField("番地",max_length=30,blank=True)
    haisou_build=models.CharField("建物名",max_length=30,blank=True)
    haisou_tel=models.CharField("電話番号",max_length=30,blank=True)
    haisou_mail=models.CharField("メールアドレス",max_length=100,blank=True)
    nouhin_com=models.CharField("納品書会社名",max_length=30,blank=True)
    nouhin_cus=models.CharField("納品書名前",max_length=30,blank=True)
    nouhin_day=models.CharField("納品書日付",max_length=30,null=True,blank=True,default="")
    rental_maxday=models.CharField("貸出期限",max_length=30,null=True,blank=True,default="")
    bikou1=models.TextField("備考（納品）",blank=True)
    bikou2=models.TextField("備考（依頼）",blank=True)
    status=models.IntegerField("状態",default=0)
    unsou_com=models.CharField("運送会社",max_length=20,null=True,blank=True,default="")
    unsou_num=models.CharField("問い合わせ番号",max_length=20,null=True,blank=True,default="")
    cancel_day=models.CharField("キャンセル日",max_length=30,null=True,blank=True,default="")
    cancel_name=models.CharField("キャンセル担当",max_length=30,null=True,blank=True,default="")

    def __str__(self):
        return str(self.irai_num)
    
    # irai_type（内容）　0:顧客　1:店舗　2:キープ
    # status（状態）　0:変更可　1:準備中　2:完了　3.キャンセル
    

class Rireki_shouhin(models.Model):
    irai_num=models.IntegerField("依頼No")
    irai_hontai_num=models.IntegerField("本体No")
    irai_hontai_kubun=models.CharField("区分",max_length=5,null=True,blank=True,default="")

    def __str__(self):
        return str(self.irai_num)