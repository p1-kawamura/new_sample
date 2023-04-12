from django.urls import path
from .views import index,csv_imp,csv_imp_page,dele,hinban_enter_ajax,hinban_click_ajax,color_size_click_ajax


app_name="zaiko"
urlpatterns = [
    path('', index, name="index"),
    path('csv_imp_page/', csv_imp_page, name="csv_imp_page"), 
    path('csv_imp/', csv_imp, name="csv_imp"),
    path('dele/', dele, name="dele"), 
    path('hinban_enter_ajax/', hinban_enter_ajax, name="hinban_enter_ajax"),
    path('hinban_click_ajax/', hinban_click_ajax, name="hinban_click_ajax"),
    path('color_size_click_ajax/', color_size_click_ajax, name="color_size_click_ajax"),
]