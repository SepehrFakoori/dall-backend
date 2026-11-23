from django.contrib import admin

from .models import Tenant, Membership


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at", "updated_at")
    search_fields = ("name",)


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ("tenant", "user", "is_active", "created_at", "updated_at")
    list_filter = ("is_active",)
    list_select_related = ("tenant", "user")
    search_fields = ("tenant__name", "user__username")
