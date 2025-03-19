from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    address = models.CharField(max_length=150,null=True,blank=True)
    contact = models.IntegerField(null=True,blank=True)
    profile_pic = models.ImageField(upload_to="profile_pics/",null=True,blank=True)



