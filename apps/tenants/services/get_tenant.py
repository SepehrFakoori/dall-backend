from django.core.cache import cache

from ..models import Tenant

TENANT_CACHE_TTL = 60  # Seconds


def _tenant_key(tenant_id):
    return f"tenant_id:{tenant_id}"


def get_tenant(tenant_id):
    key = _tenant_key(tenant_id)
    tenant = cache.get(key)
    if tenant is None:
        tenant = Tenant.objects.filter(id=tenant_id, is_active=True).first()
        if tenant:
            cache.set(key, tenant, TENANT_CACHE_TTL)
    return tenant


def invalidate_tenant_cache(tenant_id):
    cache.delete(_tenant_key(tenant_id))
