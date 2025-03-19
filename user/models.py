from django.db import models
from django.contrib.auth.models import User


# the profile model is releation to user model (oneToOne)
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    address = models.CharField(max_length=150,null=True,blank=True)
    contact = models.IntegerField(null=True,blank=True)
    profile_pic = models.ImageField(upload_to="profile_pics/",null=True,blank=True)


# category model
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
# blog model
class Blog(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='blogs')
    created_at = models.DateField(auto_now=True,null=True,blank=True)
    image = models.ImageField(upload_to="blog_img/",null=True,blank=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name="blogs")

    def __str__(self):
        return self.title

    def get_likes_count(self):
        return self.likes.count()

    def get_comments_count(self):
        return self.comments.count()


# Model to track who has viewed the blog
class BlogView(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='views')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='viewed_blogs')
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('blog', 'user')  # Ensure a user can view the blog only once


# Model to track likes on a blog
class BlogLike(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked_blogs')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('blog', 'user')  # Ensure a user can like a blog only once


# Model to track comments on a blog
class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.blog.title}'