from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView



class LoginView(APIView):
    def get(self, request):

        return Response({'status': 200})