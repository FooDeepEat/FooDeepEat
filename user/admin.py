from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Account)
admin.site.register(models.Option)
admin.site.register(models.Agree)
admin.site.register(models.Address)
