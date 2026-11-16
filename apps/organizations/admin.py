from django.contrib import admin

from .models import Organization, OrganizationMembership, OrganizationUnit


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(OrganizationMembership)
class OrganizationMembershipsAdmin(admin.ModelAdmin):
    list_display = ("id", "organization", "user", "is_active", "created_at")


@admin.register(OrganizationUnit)
class OrganizationUnitsAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "organization", "parent", "type")
