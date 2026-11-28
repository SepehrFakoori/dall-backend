from functools import cached_property

from rest_framework import serializers

from .models import Check, CheckType, CheckStatus, CheckDirection


class CheckTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckType
        fields = "__all__"


class CheckStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckStatus
        fields = "__all__"


class CheckBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Check
        fields = (
            "id",
            "purpose",
            "description",
            "sayad_id",
            "type",
            "status",
            "due_date",
            "amount",
        )


class ReceivedCheckSerializer(CheckBaseSerializer):
    class Meta(CheckBaseSerializer.Meta):
        fields = (*CheckBaseSerializer.Meta.fields, "drawer")


class IssuedCheckSerializer(CheckBaseSerializer):
    class Meta(CheckBaseSerializer.Meta):
        fields = (*CheckBaseSerializer.Meta.fields, "payee")


class CheckSerializer(CheckBaseSerializer):
    class Meta(CheckBaseSerializer.Meta):
        fields = (*CheckBaseSerializer.Meta.fields, "drawer", "payee")
        extra_kwargs = {
            "drawer": {"help_text": "Only applies to received checks."},
            "payee": {"help_text": "Only applies to issued checks."},
        }

    @cached_property
    def _serializers_by_direction(self):
        return {
            CheckDirection.RECEIVED: ReceivedCheckSerializer(context=self.context),
            CheckDirection.ISSUED: IssuedCheckSerializer(context=self.context),
        }

    def validate(self, attrs):
        check_type = attrs.get("type")
        if check_type is None and self.instance is not None:
            check_type = self.instance.type
        if check_type is None:
            return attrs

        serializer = self._serializers_by_direction.get(check_type.type)
        if serializer is None:
            raise serializers.ValidationError({"type": "Unsupported check direction."})

        excluded_fields = self.fields.keys() - serializer.fields.keys()
        invalid_fields = excluded_fields & attrs.keys()
        if invalid_fields:
            raise serializers.ValidationError(
                {
                    field: "This field does not apply to this check type."
                    for field in invalid_fields
                }
            )

        # Clear any stored party that no longer applies to this direction.
        attrs.update(dict.fromkeys(excluded_fields))
        return attrs

    def to_representation(self, instance):
        serializer = self._serializers_by_direction.get(instance.type.type)
        if serializer is None:
            serializer = CheckBaseSerializer(context=self.context)
        return serializer.to_representation(instance)
