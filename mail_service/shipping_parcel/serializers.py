from core.serializers import UserSerializer
from rest_framework import serializers

from .models import Parcel


class ParcelSerializer(serializers.ModelSerializer):
    parcel_owner = UserSerializer(required=False)

    class Meta:
        model = Parcel
        fields = "__all__"
