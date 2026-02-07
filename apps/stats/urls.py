from django.urls import path
from .views import stats

urlpatterns = [
    path('', stats, name = 'stats')
]