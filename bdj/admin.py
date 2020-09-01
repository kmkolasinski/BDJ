from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from bdj.models import FoodPlace, FoodPlaceGroup, BDJUser

admin.site.register(FoodPlace)
admin.site.register(FoodPlaceGroup)
admin.site.register(BDJUser, UserAdmin)
