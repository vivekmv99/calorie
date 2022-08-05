from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(FoodItem)
admin.site.register(Activitie)
admin.site.register(TimeSpend)