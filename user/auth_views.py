from django.shortcuts import render , redirect
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens  import RefreshToken
from django.contrib import messages
from django.contrib.auth import authenticate , logout , login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import re

       
def register_view(request):
    if request.method == 'POST':
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messages.error(request, "Enter a valid email address.")
            return redirect("user-register")
        
        if not username or not password or not email or not fname or not lname or not confirm_password:
            messages.error(request, "All fields are required")
            return redirect("user-register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken")
            return redirect("user-register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already taken")
            return redirect("user-register")
        
        if password != confirm_password:
            messages.error(request, "Password do not match")
            return redirect("user-register")


        # Create user
        user = User.objects.create_user(username=username,first_name=fname,last_name=lname,  password=password, email=email)
        user.save()

        messages.success(request, "User registered and logged in successfully!")
        return redirect("user-login")

    return render(request, "user/user_register.html")


# @csrf_exempt
# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
        

#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request,user)
#             # Generate JWT token
#             refresh = RefreshToken.for_user(user)
#             access_token = str(refresh.access_token)
            
#              # store token  in cookies 
#             response = redirect("/")
#             response.set_cookie("access_token", access_token, httponly=True,samesite="Lax",  # Prevent CSRF issues
#                 secure=False )
#             messages.success(request, "Login successful")
#             return response
#         else:
#             messages.error(request, "Invalid credentials")
#             return redirect('user-login')

#     return render(request, "user/user_login.html")


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        if not User.objects.filter(username=username).exists():
            # Display an error message if the username does not exist
            messages.error(request, 'Invalid Username')
            return redirect('user/login/')
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Log the user in
            login(request, user)

            messages.success(request, "Login successful!")
            return redirect("user-home")  # Redirect to home page
        else:
            messages.error(request, "Invalid credentials")
            return redirect("user-login")

    return render(request, "user/user_login.html")


# @csrf_exempt
# def logout_view(request):
#     if request.method == 'POST':
#         logout(request)  # End the Django session
#         response = JsonResponse({"message": "Logout successful"})
#         response.delete_cookie("access_token")  # Remove JWT from cookies
#         # messages.success(request,"Logout successfully...")
#         return response
    
# @csrf_exempt
# def logout_view(request):
#     if request.method == 'POST':
#         logout(request) 
#         response = JsonResponse({"message": "Logout successful"})
#         response.delete_cookie("sessionid")
#         return redirect('user-login')

@csrf_exempt
def logout_view(request):
    if request.method in ["POST", "GET"]:  # ✅ Handle both GET and POST
        logout(request)  # Logout the user
        response = JsonResponse({"message": "Logout successful"}, status=200)
        response.delete_cookie("sessionid")  # Remove session cookie
        return response if request.headers.get("X-Requested-With") == "XMLHttpRequest" else redirect("user-login")
