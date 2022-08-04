from os import name
from django.urls import path
from . views import *

urlpatterns = [
    path('loginApi/',LoginView.as_view())
]
