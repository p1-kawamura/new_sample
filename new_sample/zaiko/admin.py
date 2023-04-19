from django.contrib import admin
from .models import Shouhin,Rental,Size
from django.contrib.admin import ModelAdmin

class Sho(ModelAdmin):
    model=Shouhin
    list_display=["hontai_num","sample_num","shouhin_name","joutai","irai_num"]

class Ren(ModelAdmin):
    model=Rental
    list_display=["irai_num_rental","rental_day","tantou"]

class Si(ModelAdmin):
    model=Size
    list_display=["size_num","size"]

admin.site.register(Shouhin,Sho)
admin.site.register(Rental,Ren)
admin.site.register(Size,Si)