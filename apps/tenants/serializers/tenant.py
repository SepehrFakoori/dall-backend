from rest_framework import serializers

from ..models import Tenant


class CurrentTenantSerializer(serializers.ModelSerializer):
    domains = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Tenant
        fields = ["id", "name", "schema_name", "is_active", "created_at", "domains"]
        read_only_fields = ["id", "schema_name", "is_active", "created_at", "domains"]

    def get_domains(self, obj):
        return list(obj.domains.values_list("domain", flat=True))
