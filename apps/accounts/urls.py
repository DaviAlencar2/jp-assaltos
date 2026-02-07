from django.urls import path, include
from .views import login, signup, logout, profile

urlpatterns = [
    path('login/', login, name='login'),
    path('signup/', signup, name='signup'),
    path('logout/', logout, name='logout'),
    path('profile/', profile, name='profile'),
]
