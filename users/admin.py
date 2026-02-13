from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    # Fields shown in the user list page
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'phone',
        'is_staff',
        'is_active',
    )

    list_filter = (
        'is_staff',
        'is_active',
        'is_superuser',
    )

    # Fields shown when editing/creating a user
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Permissions', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )

    # Fields shown when creating a user via admin
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'email',
                'phone',
                'password1',
                'password2',
                'is_staff',
                'is_active',
            ),
        }),
    )

    search_fields = ('username', 'email', 'phone')
    ordering = ('username',)

