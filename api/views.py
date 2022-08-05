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
from .helper import *
from django.contrib.auth.hashers import make_password

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


class AddFoodItems(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        decoded = token_decode(request)
        serializer = AddFoodSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'status': False, 'message': serializer.errors})
        item = serializer.save()
        if decoded['is_admin'] == True:
            item.user = decoded['user_id']
            item.is_user = True
            item.is_global = True
        else:
            item.user = CustomUser.objects.get(id=decoded['user_id'])
            item.is_user = False
            item.is_global = False
        item.save()
        return Response({"status":True,"message":"Food Item is added successfully"})

    #requested
    def get(self, request):
        decoded = token_decode(request)
        if decoded['is_admin'] != True:
            return Response({"status": False,"message": "No access!!"})
        food_list = FoodItem.objects.filter(is_global=False,is_user=False)
        food_serializer = AdminFoodSerializer(food_list, many=True)
        return Response({"status": True,"item_list":food_serializer.data})


    def patch(self,request):
        if item_id := request.data['item_id']:
            FoodItem.objects.filter(id=item_id).update(is_global=True)
        return Response({"status":True,"message":"Item is Added to global list"})


class SignUp(APIView):
    def post(self,request):
        serializer = SignUpSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'status': False, 'message': serializer.errors})
        user = serializer.save()
        user.customer = True
        user.password = make_password(serializer.data['password'])
        user.save()
        refresh = RefreshToken.for_user(user)
        refresh['email'] = user.email
        refresh['is_admin'] = user.is_admin
        return Response({"status": True, 'refresh': str(refresh),
                         'access': str(refresh.access_token), 'message': "successfully Signed in"})

