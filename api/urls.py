from os import name
from django.urls import path
from . views import *
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('loginApi/',LoginView.as_view()),
    path('addFoodItems/',AddFoodItems.as_view()),
    path('addActivityApi/',AddActivity.as_view()),

    path('signUpApi/',SignUp.as_view()),

    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
