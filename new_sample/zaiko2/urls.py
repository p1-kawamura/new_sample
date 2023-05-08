from django.urls import path
from .views import index2,size_category

app_name="zaiko2"
urlpatterns = [
    path('index2/', index2, name="index2"),
    path('size_category/', size_category, name="size_category"),
]