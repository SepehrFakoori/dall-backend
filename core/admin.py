from django.contrib import admin


class PlatformModelAdmin(admin.ModelAdmin):
    """Keep global admin operations separate from tenant ownership and role grants."""

    def has_module_permission(self, request):
        """Show ERP models only to platform superusers."""
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        """Require platform authority to inspect global admin records."""
        return request.user.is_superuser

    def has_add_permission(self, request):
        """Allow model creation only through platform administration."""
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        """Require platform authority when changing global admin records."""
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        """Require platform authority when deleting global admin records."""
        return request.user.is_superuser

    def get_queryset(self, request):
        """Inspect platform records without relying on a tenant selection header."""
        manager = getattr(self.model, "unscoped", self.model._default_manager)
        queryset = manager.all()
        ordering = self.get_ordering(request)
        return queryset.order_by(*ordering) if ordering else queryset


class ERPReadOnlyAdmin(PlatformModelAdmin):
    """Inspect ERP records globally and keep their writes on the scoped APIs."""

    def has_add_permission(self, request):
        """Route creation through authorization-aware ERP services."""
        return False

    def has_change_permission(self, request, obj=None):
        """Route updates through authorization-aware ERP services."""
        return False

    def has_delete_permission(self, request, obj=None):
        """Route deletion through authorization-aware ERP services."""
        return False
