from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name="home"),
    path('dashboard/', dashboard, name="dashboard"),
    path('login/', user_login, name="login"),
    path('signup/', user_signup, name="signup"),
    path('logout/', user_logout, name="logout"),
    path('chat/<str:room_name>/', chat, name="chat"),
]