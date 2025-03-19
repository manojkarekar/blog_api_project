from rest_framework import serializers,status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .auth_serializers import *
from django.contrib.auth import login , logout
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from django.http import JsonResponse
from django.middleware.csrf import get_token
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.models import Token

#user register api views

class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'message': 'User registered successfully!',
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# user login api views
class LoginAPIView(APIView):
    def post(self, request):
        
        if request.user.is_authenticated:
            return Response({'message': f'You are already logged in , {request.user.username}'}, status=status.HTTP_200_OK)

        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user) 
            token, _ = Token.objects.get_or_create(user=user)
            response  = Response({'message': 'Login successful!', 'token': token.key}, status=status.HTTP_200_OK)
            response.set_cookie("sessionid", request.session.session_key, httponly=True, samesite="Lax")
            return response
        
        return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


# test api views after user is login
class IndexView(APIView):
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated] 

    def get(self, request):
        # You can access the user info via request.user
        return Response({'message': "User home page"}, status=status.HTTP_200_OK)
   
# show all user accounts details api views 
class ListUsers(APIView): 
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated] 
    def get(self,request):
        users  = User.objects.all()
        data = UserSerializer(users,many=True).data
        return Response(data)



# user logout api views
@method_decorator(csrf_exempt, name='dispatch')
class LogoutAPIView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication] 
    permission_classes = [IsAuthenticated] 

    def post(self, request):
        request.user.auth_token.delete() 
        logout(request) 
        response = Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
        response.delete_cookie("sessionid")
        return response

class CSRFTokenAPIView(APIView):
    def get(self, request):
        csrf_token = get_token(request)
        return Response({'csrf_token': csrf_token}) 
    

@method_decorator(csrf_exempt, name='dispatch')
class CheckLoginAPIView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            return Response({'logged_in': True, 'username': request.user.username}, status=200)
        return Response({'logged_in': False}, status=401)