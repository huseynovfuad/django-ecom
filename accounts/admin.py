from django.contrib import admin
from .models import Profile, DeletedProfile

# Register your models here.

admin.site.register(Profile)
admin.site.register(DeletedProfile)
