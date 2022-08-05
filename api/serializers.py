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