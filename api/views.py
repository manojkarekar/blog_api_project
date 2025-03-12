from rest_framework import serializers,status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .auth_serializers import *
from django.contrib.auth import login , logout
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticated

#user register api views
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

# user login api views
class LoginAPIView(APIView):
    def post(self, request):
        
        if request.user.is_authenticated:
            return Response({'message': 'You are already logged in.'}, status=status.HTTP_200_OK)

        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user) 
            response = Response({'message': 'Login successful!'}, status=status.HTTP_200_OK)
            return response
        
        return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


# test api views after user is login
class IndexView(APIView):
    permission_classes = [IsAuthenticated] 

    def get(self, request):
        # You can access the user info via request.user
        return Response({'message': "User home page"}, status=status.HTTP_200_OK)
   
# show all user accounts details api views 
class ListUsers(APIView): 
    permission_classes = [IsAuthenticated] 
    def get(self,request):
        users  = User.objects.all()
        data = UserSerializer(users,many=True).data
        return Response(data)


# user logout api views
class LogoutAPIView(APIView):
    def post(self, request):
        logout(request)  # End session

        response = Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
        response.delete_cookie("access_token")  # Remove token
        return response
