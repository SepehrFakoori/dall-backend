from django.contrib import admin

from .models import (
    Organization,
    OrganizationMembership,
    Department,
    DepartmentMembership,
)


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(OrganizationMembership)
class OrganizationMembershipAdmin(admin.ModelAdmin):
    list_display = ("organization", "user", "is_active")
    list_filter = ("is_active",)
    list_select_related = ("organization", "user")
    # raw_id_fields = ("organization", "user")
    search_fields = ("organization__name", "user__username")


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(DepartmentMembership)
class DepartmentMembershipAdmin(admin.ModelAdmin):
    list_display = ("department", "user")
    list_select_related = ("department", "user")
    # raw_id_fields = ("department", "user")
    search_fields = ("department__name", "user__username")
