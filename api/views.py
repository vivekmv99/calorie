from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from . permissions import CustomPermission
from .serializers import *
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'status': False, 'error': serializer.errors})
        email = serializer.data['email']
        password = serializer.data['password']
        if user := authenticate(email=email, password=password):
            refresh = RefreshToken.for_user(user)
            refresh['email'] = user.email
            refresh['is_admin'] = user.is_admin
            return Response({"status":True,'refresh': str(refresh),
                         'access': str(refresh.access_token),'message':"successfully logged in"})
        else:
            return Response({"status":False,'message':'wrong email or password'})