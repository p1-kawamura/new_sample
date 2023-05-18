from django.contrib import admin
from .models import Shouhin,Rental,Size,Shozoku,Rireki_rental,Rireki_shouhin,Category,Label
from django.contrib.admin import ModelAdmin

class A_shouhin(ModelAdmin):
    model=Shouhin
    list_display=["hontai_num","sample_num","shouhin_name","joutai","irai_num"]

class A_rental(ModelAdmin):
    model=Rental
    list_display=["irai_num_rental","rental_day","tantou"]

class A_size(ModelAdmin):
    model=Size
    list_display=["size_num","size"]

class A_category(ModelAdmin):
    model=Category
    list_display=["category_num","category","category_ex"]

class A_shozoku(ModelAdmin):
    model=Shozoku
    list_display=["shozoku"]

class A_rireki_rental(ModelAdmin):
    model=Rireki_rental
    list_display=["irai_num","irai_type","rental_day","tantou","haisou_cus","haisou_tempo","status"]

class A_Rireki_shouhin(ModelAdmin):
    model=Rireki_shouhin
    list_display=["irai_num","irai_hontai_num"]

class A_Label(ModelAdmin):
    model=Label
    list_display=["sample_num","shouhin_num"]


admin.site.register(Shouhin,A_shouhin)
admin.site.register(Rental,A_rental)
admin.site.register(Size,A_size)
admin.site.register(Category,A_category)
admin.site.register(Shozoku,A_shozoku)
admin.site.register(Rireki_rental,A_rireki_rental)
admin.site.register(Rireki_shouhin,A_Rireki_shouhin)
admin.site.register(Label,A_Label)

