import datetime

from rest_framework import serializers

from core.serializers import UserSerializer

from .models import Parcel, Train, TrainTrack


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


class TrainTrackSerializer(serializers.ModelSerializer):
    is_busy = serializers.SerializerMethodField()

    class Meta:
        model = TrainTrack
        fields = ("created", "source", "destination", "is_busy")

    def get_is_busy(self, obj):
        current_time = datetime.datetime.now()
        if (
            obj.shipped_track.first()
            and obj.shipped_track.first().created + datetime.timedelta(hours=3)
            > current_time
        ):
            return True
        return False
