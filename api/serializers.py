from django.contrib.auth import authenticate
from .models import *
from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=400)
    password = serializers.CharField(max_length=200)

class AddFoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItem
        fields = ('name','carbohydrate','fats','protein','calorie')

class AdminFoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItem
        fields = "__all__"

def required(value):
    if value is None:
        raise serializers.ValidationError('This field is required')
class SignUpSerializer(serializers.ModelSerializer):
    name = serializers.CharField(validators=[required])
    phone = serializers.CharField(validators=[required])
    password = serializers.CharField(validators=[required])
    class Meta:
        model = CustomUser
        fields = ('email','password','name','phone')


class AddActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activitie
        fields = ('name','time','burnout')

class AdminActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItem
        fields = "__all__"