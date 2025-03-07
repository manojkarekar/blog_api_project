from django.shortcuts import render , redirect
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens  import RefreshToken
from django.contrib import messages
from django.contrib.auth import authenticate , logout , login
from django.http import JsonResponse


       
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")

        if not username or not password or not email:
            messages.error(request,"all fields are required")
            return redirect("user-register")

        if User.objects.filter(username=username).exists():
            messages.error(request,"username is already exists")
            return redirect("user-register")

        if User.objects.filter(email=email).exists():
            messages.error(request,"email is already exists")
            return redirect("user-register")
        
        user = User.objects.create_user(username=username,password=password,email=email)


        # generate jwt token 
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        messages.success(request,"user register successfully...")
        return redirect("user-login")
    
    return render(request,"user/user_register.html")

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            # Generate JWT token
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            
             # store token  in cookies 
            response = redirect("/")
            response.set_cookie("access_token", access_token, httponly=True,samesite="Lax",  # Prevent CSRF issues
                secure=False )
            messages.success(request, "Login successful")
            return response
        else:
            messages.error(request, "Invalid credentials")
            return redirect('user-login')

    return render(request, "user/user_login.html")
   


def logout_view(request):
    logout(request)  # End the Django session
    response = JsonResponse({"message": "Logout successful"})
    response.delete_cookie("access_token")  # Remove JWT from cookies
    return redirect("user-login")