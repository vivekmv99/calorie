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
from datetime import date
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
        item.user = CustomUser.objects.get(id=decoded['user_id'])
        if decoded['is_admin'] == True:
            item.is_user = True
            item.is_global = True
        else:
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
        decoded = token_decode(request)
        if decoded['is_admin'] != True:
            return Response({"status": False, "message": "No access!!"})
        if item_id := request.data['item_id']:
            FoodItem.objects.filter(id=item_id).update(is_global=True)
        return Response({"status":True,"message":"Item is Added to global list"})



class AddActivity(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        decoded = token_decode(request)
        serializer = AddActivitySerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'status': False, 'message': serializer.errors})
        activity = serializer.save()
        activity.user = CustomUser.objects.get(id=decoded['user_id'])
        if decoded['is_admin'] == True:
            activity.is_user = True
            activity.is_global = True
        else:
            activity.is_user = False
            activity.is_global = False
        activity.save()
        return Response({"status": True, "message": "Food Item is added successfully"})

    # requested
    def get(self, request):
        decoded = token_decode(request)
        if decoded['is_admin'] != True:
            return Response({"status": False, "message": "No access!!"})
        activity_list = Activitie.objects.filter(is_global=False, is_user=False)
        activity_serializer = AdminActivitySerializer(activity_list, many=True)
        return Response({"status": True, "activty_list": activity_serializer.data})

    def patch(self, request):
        decoded = token_decode(request)
        if decoded['is_admin'] != True:
            return Response({"status": False, "message": "No access!!"})
        if activity_id := request.data['activity_id']:
            Activitie.objects.filter(id=activity_id).update(is_global=True)
        return Response({"status": True, "message": "Activity is Added to global list"})


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



#user
class FoodList(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        food_list = FoodItem.objects.filter(is_global=True)
        food_serializer = AddFoodSerializer(food_list, many=True)
        return Response({"status": True, "item_list": food_serializer.data})

    def post(self,request):
        try:
            food_id = request.data['food_id']
            consumed = request.data['consumed']
        except:
            food_id,consumed=None,None
        decoded = token_decode(request)
        if food_id and consumed :
            try:
                food = FoodItem.objects.get(id=food_id)
            except:
                food = None
            if food:
                FoodConsumed(food_id=food_id,amount=consumed,user_id=decoded['user_id']).save()
                return Response({'status': True, 'message': "Added successfully"})
            else:
                return Response({"status": False, "message": "No activity found"})
        else:
            return Response({"status": False, "message": "something went wrong"})


class ActivityList(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        activity_list = Activitie.objects.filter(is_global=True)
        activity_serializer = AddActivitySerializer(activity_list, many=True)
        return Response({"status": True, "item_list": activity_serializer.data})

    def post(self,request):
        try:
            activity_id = request.data['activity_id']
            spend = request.data['spend']
        except:
            activity_id,spend=None,None
        decoded = token_decode(request)
        if activity_id and spend :
            try:
                act = Activitie.objects.get(id=activity_id)
            except:
                act = None
            if act:
                TimeSpend(activity_id=activity_id,time=spend,user_id=decoded['user_id']).save()
                return Response({'status': True, 'message': "Added successfully"})
            else:
                return Response({"status": False, "message": "No activity found"})
        else:
            return Response({"status": False, "message": "something went wrong"})




class StatsList(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        try:
            start_date = request.data['start_date']
            end_date = request.data['end_date']

            todayz = request.data['today']
        except:
            start_date,end_date,todayz=None,None,None
        decoded = token_decode(request)
        if todayz == "True":
            today = date.today()
            stats,consumed_list,activity_list = [],[],[]
            consumed = FoodConsumed.objects.filter(user=decoded['user_id'], created_at__year=today.year,
                                                   created_at__month=today.month, created_at__day=today.day)
            activity = TimeSpend.objects.filter(user=decoded['user_id'], created_at__year=today.year,
                                                   created_at__month=today.month, created_at__day=today.day)
            for i in consumed:
                gain = i.food.calorie * i.amount
                val = {
                    'Food You Consumed':i.food.name,
                    'Consumed Amount':i.amount,
                    'This food Contains':f"{i.food.carbohydrate} :carbohydrate,{i.food.fats} : fat,{i.food.protein} : protein,{i.food.calorie}:calorie",
                    'You Gained': f"{gain}:calorie"
                }
                consumed_list.append(val)
            for i in activity:
                burn = i.time * i.activity.burnout
                val_two = {
                    'Activity you have done':i.activity.name,
                    'Time spend':f"{i.time}hrs",
                    'This workout burned':f"{burn}calorie"
                }
                activity_list.append(val_two)
            stats = {
                'consumed':consumed_list,
                'activity':activity_list
            }
            return Response({'status': True, 'message': "","consumed":stats})
        elif start_date and end_date:
            print(start_date,end_date)
        else:
            return Response({'status': False,"message":"something wrong"})



