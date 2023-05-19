from django.urls import path
from .views import index2,category_click_ajax,hinban_click_ajax,list_click_ajax,ikkatsu_hinban,ikkatsu_del,sample_num_auto,\
                    kobetsu_del,kobetsu_up,label_add,label_print,\
                    size_category,size_num,size_name,size_new,category_num,category_name,category_new

app_name="zaiko2"
urlpatterns = [
    path('index2/', index2, name="index2"),
    path('category_click_ajax/', category_click_ajax, name="category_click_ajax"),
    path('hinban_click_ajax/', hinban_click_ajax, name="hinban_click_ajax"),
    path('list_click_ajax/', list_click_ajax, name="list_click_ajax"),
    path('ikkatsu_hinban/', ikkatsu_hinban, name="ikkatsu_hinban"),
    path('ikkatsu_del/', ikkatsu_del, name="ikkatsu_del"),
    path('sample_num_auto/', sample_num_auto, name="sample_num_auto"),
    path('kobetsu_del/', kobetsu_del, name="kobetsu_del"),
    path('kobetsu_up/', kobetsu_up, name="kobetsu_up"),
    path('label_add/', label_add, name="label_add"),
    path('label_print/', label_print, name="label_print"),
    path('size_category/', size_category, name="size_category"),
    path('size_num/', size_num, name="size_num"),
    path('size_name/', size_name, name="size_name"),
    path('size_new/', size_new, name="size_new"),
    path('category_num/', category_num, name="category_num"),
    path('category_name/', category_name, name="category_name"),
    path('category_new/', category_new, name="category_new"),
]