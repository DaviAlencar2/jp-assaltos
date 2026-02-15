from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name = "home"),
    path('add/', add, name = "add" ),
    path('dados/<int:year>/', data_by_year, name = 'dados_ano' ), 
    path('ping/', ping, name = 'ping' ),
    path('delete/<int:robbery_id>/', delete_robbery, name='delete_robbery'),
]
