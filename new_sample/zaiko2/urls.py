from django.urls import path
from .views import index2,size_category,size_num,size_name,size_new

app_name="zaiko2"
urlpatterns = [
    path('index2/', index2, name="index2"),
    path('size_category/', size_category, name="size_category"),
    path('size_num/', size_num, name="size_num"),
    path('size_name/', size_name, name="size_name"),
    path('size_new/', size_new, name="size_new"),
]