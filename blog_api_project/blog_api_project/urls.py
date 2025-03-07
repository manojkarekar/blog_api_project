from django.contrib import admin
from django.urls import path , include

urlpatterns = [
    path("admin/", admin.site.urls),

    # api app urls 
    path("api/",include("api.urls")),

    # user app urls
    path("",include("user.urls"))
]
