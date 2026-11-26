from django.contrib import admin
from django_tenants.admin import TenantAdminMixin

from .models import Domain, Tenant, Membership


class DomainInline(admin.TabularInline):
    model = Domain
    extra = 0


@admin.register(Tenant)
class TenantAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ("id", "schema_name", "name", "created_at", "updated_at")
    list_filter = ("is_active",)
    search_fields = ("name", "schema_name")
    readonly_fields = ("id", "created_at", "updated_at")
    inlines = [DomainInline]

    def get_readonly_fields(self, request, obj=None):
        fields = super().get_readonly_fields(request, obj)
        if obj:
            return (*fields, "schema_name")
        return fields


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ("user", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("user__username",)
