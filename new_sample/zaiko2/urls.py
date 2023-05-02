from django.urls import path
from .views import index2

app_name="zaiko2"
urlpatterns = [
    path('index2/', index2, name="index2"),
]