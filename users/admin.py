from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    # Add birth_date to the fieldsets
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Fields', {'fields': ('birth_date',)}),
    )
    
    # Add birth_date to the list display
    list_display = UserAdmin.list_display + ('birth_date', 'is_adult')

admin.site.register(User, CustomUserAdmin)