from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Team

class UserAdmin(BaseUserAdmin):
    # Define a new User admin
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_verified', 'is_staff')
    list_filter = ('is_active', 'is_verified', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'password', 'first_name', 'last_name', 'is_active', 'is_verified', 'is_staff', 'team')}),
        ('Permissions', {'fields': ('is_superuser', 'groups', 'user_permissions')}),
        # If you have a field for date when the user was created, include it here, else remove this line
        # ('Important dates', {'fields': ('last_login',)}), 
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'is_active', 'is_verified', 'is_staff', 'team'),
        }),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

# Register the new UserAdmin
admin.site.register(User, UserAdmin)

# TeamAdmin remains unchanged
class TeamAdmin(admin.ModelAdmin):
    list_display = ('domain',)

# Register the Team admin
admin.site.register(Team, TeamAdmin)
