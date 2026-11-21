from rest_framework import serializers

from ..models import City, Location, Province


class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = "__all__"


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = "__all__"


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"
        extra_kwargs = {
            "province": {"required": True, "allow_null": False},
            "city": {"required": True, "allow_null": False},
        }

    def validate(self, attrs):
        errors = {}
        latitude = attrs.get("latitude", getattr(self.instance, "latitude", None))
        longitude = attrs.get("longitude", getattr(self.instance, "longitude", None))
        if latitude is None and longitude is not None:
            errors["latitude"] = "Provide a latitude when longitude is set."
        if longitude is None and latitude is not None:
            errors["longitude"] = "Provide a longitude when latitude is set."
        if errors:
            raise serializers.ValidationError(errors)
        return attrs
