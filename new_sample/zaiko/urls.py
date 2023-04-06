from django.urls import path
from .views import index,csv_imp,csv_imp_page,dele


app_name="zaiko"
urlpatterns = [
    path('', index, name="index"),
    path('csv_imp_page/', csv_imp_page, name="csv_imp_page"), 
    path('csv_imp/', csv_imp, name="csv_imp"),
    path('dele/', dele, name="dele"), 
]