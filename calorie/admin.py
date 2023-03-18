from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Food)
admin.site.register(models.FoodImage)
admin.site.register(models.UserFood)
admin.site.register(models.UserMemo)
