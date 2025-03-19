from django.urls import path 
from .views import *

from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('index/', IndexView.as_view(), name='home'),
    
    path('logout/', LogoutAPIView.as_view(), name='logout'),

# all_users
    path('users/', ListUsers.as_view(), name='users'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('csrf/token/',CSRFTokenAPIView.as_view(), name='token_refresh'),
    path("check-login/",CheckLoginAPIView.as_view(),name="check-user-login")
    

]
