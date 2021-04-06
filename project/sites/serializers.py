from rest_framework import serializers
from .models import Sites


class SiteSerializers(serializers.ModelSerializer):

    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Sites
        fields = "__all__"
