from django.contrib import admin

from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "serial",
        "title",
        "name",
        "description",
        "created_at",
        "updated_at",
    )
