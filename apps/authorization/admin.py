from django.contrib import admin

from .models import Permission, Role, UserRole


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "created_at")


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "assigned_at")
