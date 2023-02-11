from django.contrib.auth.models import AbstractUser

# Create your models here.
from django.db import models


class User(AbstractUser):
    """A user in the system. Users in this system can all theoretically upload or edit essays. Everyone has the
    same level of access, for the sake of simplicity. Users need to be authenticated to do anything in the system
    other than login.

    This class is defined according to Django recommendations to allow additional fields to be added to our
    User class. Reference settings.
    """

    USER_TYPE_CHOICES = (
        ("PARCEL_OWNER", "PARCEL_OWNER"),
        ("TRAIN_OPERATOR", "TRAIN_OPERATOR"),
        ("POST_MASTER", "POST_MASTER"),
    )

    user_type = models.CharField(choices=USER_TYPE_CHOICES, max_length=20)

    class Meta:
        db_table = "user"

    def __str__(self):
        return f"user:- {self.pk}"
