from django.contrib import admin

from .models import Organization, OrganizationMembership


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
