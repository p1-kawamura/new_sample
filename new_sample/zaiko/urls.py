from django.urls import path
from .views import index


app_name="zaiko"
urlpatterns = [
    path('', index, name="index"),  
]