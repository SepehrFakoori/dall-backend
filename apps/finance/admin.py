from django.contrib import admin

from .models import BankAccount, Check


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ("bank_name", "account_number")


@admin.register(Check)
class CheckAdmin(admin.ModelAdmin):
    pass
