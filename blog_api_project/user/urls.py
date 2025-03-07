from django.urls import path 
from .auth_views import *
from .views import *

urlpatterns = [
    path("user/register/",register_view,name="user-register"),
    path("user/login/",login_view,name="user-login"),
    path("user/logout/",logout_view,name="user-logout"),
    path("",index,name="index")
]
