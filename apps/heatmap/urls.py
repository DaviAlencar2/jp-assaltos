from django.urls import path
from .views import home, add, data_by_year, ping

urlpatterns = [
    path('', home, name = "home"),
    path('add/', add, name = "add" ),
    path('dados/<int:year>/', data_by_year, name = 'dados_ano' ), 
    path('ping/', ping, name = 'ping' ),
]
