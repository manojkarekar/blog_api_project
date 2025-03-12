from rest_framework import serializers,status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .auth_serializers import *
from django.contrib.auth import login , logout
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticated


# from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken


class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'message': 'User registered successfully!'
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# api_views.py (Django API views for login)

class LoginAPIView(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            return Response(
                {'message': 'You are already logged in.'},
                status=status.HTTP_200_OK
            )

        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # Log the user in via Django session

            # Generate JWT token
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response(
                {'message': 'Login successful!', 'access_token': access_token},
                status=status.HTTP_200_OK
            )
        return Response(
            {'message': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )


class IndexView(APIView):
    permission_classes = [IsAuthenticated] 

    def get(self, request):
        # You can access the user info via request.user
        return Response({'message': "User home page"}, status=status.HTTP_200_OK)

# @api_view(["GET"])
# def all_users(request):
#     user_data = User.objects.all()
#     users  = UserSerializer(user_data,many=True)
#     return Response(users,status=status.HTTP_204_NO_CONTENT)    


class ListUsers(APIView):
   
    permission_classes = [IsAuthenticated] 
    def get(self,request):
        users  = User.objects.all()
        data = UserSerializer(users,many=True).data
        return Response(data)



class LogoutAPIView(APIView):
    def post(self, request):
        # Log the user out (removes session)
        logout(request)

        return Response(
            {'message': 'Logout successful'},
            status=status.HTTP_200_OK
        )
