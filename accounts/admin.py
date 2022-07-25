from django.contrib import admin
from .models import User


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Клиент"""
    list_display = ('first_name', 'last_name', 'username', 'password', 'description', 'is_staff')
