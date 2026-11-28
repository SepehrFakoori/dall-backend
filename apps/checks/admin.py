from django.contrib import admin

from .models import CheckType, CheckStatus, Check


@admin.register(CheckType)
class CheckAdmin(admin.ModelAdmin):
    pass


@admin.register(CheckStatus)
class CheckAdmin(admin.ModelAdmin):
    pass


@admin.register(Check)
class CheckAdmin(admin.ModelAdmin):
    pass
