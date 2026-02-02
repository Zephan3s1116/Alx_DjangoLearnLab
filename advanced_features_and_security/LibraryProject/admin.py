from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    """
    Custom admin interface for CustomUser model.
    """
    model = CustomUser
    
    # Fields to display in the list view
    list_display = ['username', 'email', 'first_name', 'last_name', 'date_of_birth', 'is_staff']
    
    # Fields to use in the detail/edit view
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('date_of_birth', 'profile_photo')}),
    )
    
    # Fields to use when creating a new user
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('date_of_birth', 'profile_photo')}),
    )

# Register the CustomUser model with the custom admin
admin.site.register(CustomUser, CustomUserAdmin)
