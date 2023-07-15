from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
usuario = get_user_model()

# Register your models here.

admin.site.register(usuario)
