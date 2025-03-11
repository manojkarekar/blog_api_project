from django.shortcuts import render
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import AnonymousUser




def index(request):
    auth = JWTAuthentication()
    user = AnonymousUser()  # Default to unauthenticated user

    try:
        # Read token from Authorization header (Bearer Token)
        token = request.headers.get("Authorization")
        if token and token.startswith("Bearer "):
            token = token.split(" ")[1]  # Extract the actual token
            validated_token = auth.get_validated_token(token)  # Validate JWT token
            user = auth.get_user(validated_token)  # Get user from token
    except AuthenticationFailed:
        pass  # Authentication failed, user remains anonymous

    return render(request, "user/index.html", {"user": user})
