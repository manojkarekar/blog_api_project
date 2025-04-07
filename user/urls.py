from django.urls import path 
from .auth_views import *
from .views import *

urlpatterns = [
    path("user/register/",register_view,name="user-register"),
    path("user/login/",login_view,name="user-login"),
    path("user/logout/",logout_view,name="logout"),
    path("",index,name="index"),
    path("user/profile/",user_profile,name="user-profile"),


    # path('blogs/', blog_list, name='blog-list'),
     path('blogs/create/', create_blog, name='create-blog'),
     
    path('blogs/<int:blog_id>/edit/',edit_blog, name='edit-blog'),
    path('blogs/<int:blog_id>/', blog_detail, name='blog-detail'),
    path('blogs/<int:blog_id>/like/', like_blog, name='like-blog'),
    path('blogs/<int:blog_id>/comment/', add_comment, name='add-comment'),

       path('like-blog/<int:blog_id>/', like_blog, name='like-blog'),
]
