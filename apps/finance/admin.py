from django.contrib import admin

from .models import Bank, Check


@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ("name", "account_number")


@admin.register(Check)
class CheckAdmin(admin.ModelAdmin):
    pass
