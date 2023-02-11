from django.db import models


class TimeStampModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    updated = models.DateTimeField(auto_now=True, db_index=True)
    objects = models.Manager()  # The default manager.

    class Meta:
        abstract = True


class TrainTrack(TimeStampModel):
    source = models.CharField(max_length=255, help_text="the source name of the track")
    destination = models.CharField(
        max_length=255, help_text="the destination name of the track"
    )
    is_busy = models.BooleanField(
        default=False,
        help_text="by default it is False when post master assigned the lines for any train it will update to True and after three hours it will automatically update to False",
    )
    objects = models.Manager()  # The default manager.


class Parcel(TimeStampModel):
    parcel_owner = models.ForeignKey(
        "core.User",
        on_delete=models.CASCADE,
        help_text="the owner of the parcel who create a parcel for shipping.",
    )
    parcel_name = models.CharField(max_length=255, db_index=True)
    parcel_weight = models.DecimalField(
        max_digits=12, decimal_places=2, help_text="weight of the parcel in Kg"
    )
    parcel_volume = models.DecimalField(
        max_digits=12, decimal_places=2, help_text="volume of the parcel in cm^3"
    )
    withdraw_bids = models.BooleanField(
        default=False,
        help_text="by default it is False when user create a parcel if user withdraw for some reason it will update to True.",
    )
    objects = models.Manager()  # The default manager.

    class Meta:
        db_table = "parcel"

    def __str__(self):
        return f"parcel:- {self.parcel_name}"


class Train(TimeStampModel):
    train_operator = models.ForeignKey(
        "core.User",
        on_delete=models.CASCADE,
        help_text="the operator of the train who can posts an offer for a train",
    )
    train_name = models.CharField(max_length=255, help_text="The name of the train")
    capacity = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="capacity of the train",
    )
    cost = models.DecimalField(
        max_digits=12, decimal_places=2, help_text="the cost of the shipping"
    )
    is_available = models.BooleanField(
        default=True,
        help_text="by default it is True it will update to False when the train will shipped.",
    )
    withdraw_bids = models.BooleanField(
        default=False,
        help_text="by default it is False when Train Operator posts an offer for a train if user withdraw for some reason it will update to True.",
    )
    lines_they_operate = models.ManyToManyField(
        "TrainTrack",
        related_name="operate_track",
        help_text="assigned all lines that train operator can operate",
    )
    objects = models.Manager()  # The default manager.

    class Meta:
        db_table = "Train"

    def __str__(self):
        return f"Train:- {self.train_name}"


class ShippedParcel(TimeStampModel):
    train = models.ForeignKey(
        "Train", on_delete=models.CASCADE, related_name="shipped_train"
    )
    parcel = models.ForeignKey(
        "Parcel", on_delete=models.CASCADE, related_name="shipped_parcel"
    )
    assigned_lines = models.ForeignKey(
        "TrainTrack", on_delete=models.CASCADE, related_name="shipped_track"
    )
    objects = models.Manager()  # The default manager.

    class Meta:
        db_table = "ShippedParcel"
