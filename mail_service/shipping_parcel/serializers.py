from rest_framework import serializers

from core.serializers import UserSerializer

from .models import Parcel, Train


class ParcelSerializer(serializers.ModelSerializer):
    parcel_owner = UserSerializer(required=False)

    class Meta:
        model = Parcel
        fields = "__all__"


class PostTrainOfferSerializer(serializers.ModelSerializer):
    train_operator = UserSerializer(required=False)

    class Meta:
        model = Train
        fields = "__all__"
