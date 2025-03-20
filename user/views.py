from django.shortcuts import render , redirect , get_object_or_404
from .forms import ProfileForm , CommentForm , BlogForm
from .models import Profile , BlogLike ,Blog ,Comment , BlogView
from django.contrib.auth.decorators import login_required


def index(request):
    blogs = Blog.objects.all().order_by('-created_at')
    
    # Track blog views for the current user
    for blog in blogs:
        BlogView.objects.get_or_create(blog=blog, user=request.user)
    
    # Handle comment and like actions for each blog
    if request.method == 'POST':
        if 'comment' in request.POST:
            # Handle comment submission
            blog_id = request.POST.get('blog_id')
            blog = Blog.objects.get(id=blog_id)
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.blog = blog
                comment.user = request.user
                comment.save()
        # elif 'like' in request.POST:
        #     # Handle like submission
        #     blog_id = request.POST.get('blog_id')
        #     blog = Blog.objects.get(id=blog_id)
        #     BlogLike.objects.get_or_create(blog=blog, user=request.user)
    
    # Get comments, likes, and view data for each blog
    blogs_data = []
    for blog in blogs:
        blog_likes = BlogLike.objects.filter(blog=blog)
        # user_liked = BlogLike.objects.filter(blog=blog, user=request.user).exists()
        comments = Comment.objects.filter(blog=blog)
        blogs_data.append({
            'blog': blog,
            'likes_count': blog_likes.count(),
            # 'user_liked': user_liked,
            'comments': comments,
        })

    return render(request, "user/index.html", {
        'blogs_data': blogs_data,
        'form': CommentForm(),  # For adding comments
    })


@login_required
def user_profile(request):
    user = request.user  # get the login user
    profile, created = Profile.objects.get_or_create(user=user)  #get or create a user profile

    if request.method == 'POST':
        # Pass the user to the form
        form = ProfileForm(request.POST, request.FILES, instance=profile, user=user)
        if form.is_valid():
            # Save the user-specific fields first
            user.username = form.cleaned_data['username']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()

            # Save the profile fields
            form.save()

            return redirect('/')  # Redirect to the same page after saving

    else:
        # Pass the user to pre-fill form
        form = ProfileForm(instance=profile, user=user)

    return render(request, "user/pages/user_profile.html", {
        "form": form,  # The form with both user and profile fields
        "user": user,  # Pass the user data to the template
    })


@login_required
def create_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)  # Ensure we handle file uploads
        if form.is_valid():
            blog = form.save(commit=False)
            blog.user = request.user  # Set the current user as the blog author
            blog.save()
            return redirect('blog-detail', blog_id=blog.id)  # Redirect to the newly created blog's detail page
    else:
        form = BlogForm()

    return render(request, 'user\pages\create_blog.html', {'form': form})

@login_required
def edit_blog(request, blog_id):
    blog = Blog.objects.get(id=blog_id)

    if request.user != blog.user:
        # Ensure only the blog owner can edit the blog
        return redirect('blog-detail', blog_id=blog.id)

    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)  # Include the existing blog data
        if form.is_valid():
            form.save()
            return redirect('blog-detail', blog_id=blog.id)  # Redirect to the blog's detail page
    else:
        form = BlogForm(instance=blog)

    return render(request, 'edit_blog.html', {'form': form, 'blog': blog})

@login_required
def like_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    print(blog)
    
    # If the user has already liked this blog, don't do anything
    if BlogLike.objects.filter(user=request.user,blog=blog).exists():
        like = BlogLike.objects.filter(user=request.user,blog=blog).first()
        if like:
            like.delete()
          
    else:
        BlogLike.objects.create(user=request.user,blog=blog)
          
    return redirect("/")


@login_required
def add_comment(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = blog
            comment.user = request.user
            comment.save()
            return redirect('blog-detail', blog_id=blog.id)
    else:
        form = CommentForm()

    return render(request, 'add_comment.html', {'form': form, 'blog': blog})


@login_required
def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)

    # Track the view
    BlogView.objects.get_or_create(blog=blog, user=request.user)
    
    # Handle comment submission
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = blog
            comment.user = request.user
            comment.save()

    # Handle likes
    blog_likes = BlogLike.objects.filter(blog=blog)
    user_liked = BlogLike.objects.filter(blog=blog, user=request.user).exists()

    comments = Comment.objects.filter(blog=blog)

    return render(request, 'user/pages/blog_detail.html', {
        'blog': blog,
        'comments': comments,
        'form': CommentForm(),
        'likes': blog_likes.count(),
        'user_liked': user_liked,
    })
