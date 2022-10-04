from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model


@admin.register(get_user_model())
class CustomUserAdmin(UserAdmin):
    model = get_user_model()
    list_display = ('username', 'title', 'role',
                    'email', 'is_staff', 'is_active',)
