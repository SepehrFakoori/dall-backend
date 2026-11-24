from django.contrib import admin

from .models import Department, DepartmentMembership


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(DepartmentMembership)
class DepartmentMembershipAdmin(admin.ModelAdmin):
    list_display = ("department", "membership", "created_at", "updated_at")
    list_select_related = ("department", "membership")
    search_fields = ("department__name", "membership__username")
