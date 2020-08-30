from django.contrib import admin

# Register your models here.
from bdj.models import FoodPlace, FoodPlaceGroup

admin.site.register(FoodPlace)
admin.site.register(FoodPlaceGroup)
