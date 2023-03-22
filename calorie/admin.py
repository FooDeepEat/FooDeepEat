from django.contrib import admin
from . import models


# Register your models here.


@admin.register(models.Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ('name', 'carbohydrate', 'protein', 'fat', 'created_at')
    list_filter = ('name', 'created_at')


@admin.register(models.FoodImage)
class FoodImageAdmin(admin.ModelAdmin):
    list_display = ('name', 'food_img', 'created_at')
    list_filter = ('name', 'created_at')


admin.site.register(models.UserFood)
admin.site.register(models.UserMemo)
