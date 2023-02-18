from django.db.models import F
from rest_framework import generics, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Parcel, ShippedParcel, Train, TrainTrack
from .permissions import (ParcelPermissions, PostMasterPermissions,
                          TrainPermissions)
from .serializers import (BookedTrainListSerializer,
                          BookTrainAndShippedSerializer, ParcelSerializer,
                          PostTrainOfferSerializer, TrainTrackSerializer)
from .utils import get_parcel_shipped_data, get_train_shipped_data


class ParcelView (generics.ListCreateAPIView):
    queryset=Parcel.objects.select_related ("parcel_owner")
    permission_classes=(IsAuthenticated, ParcelPermissions)
    serializer_class=ParcelSerializer
    pagination_class=LimitOffsetPagination

    __doc__="""
    GET: This api is used to return the list of all parcel list of the logged in parcel owner only parcel owner or post master can access this api.
    POST: This api is used to create a new parcel for ship only parcel owner user can access this api.
        params:
           parcel_name: CharField,
           parcel_weight: DecimalField,
           parcel_volume: DecimalField
    """

    def perform_create(self, serializer):
        serializer.save (parcel_owner=self.request.user)

    def get_queryset(self):
        if self.request.user.user_type == "POST_MASTER":
            return self.queryset.filter (
                withdraw_bids=False, shipped_parcel=None
            ).select_related ("parcel_owner")
        return self.queryset.filter (
            parcel_owner=self.request.user, withdraw_bids=False, shipped_parcel=None
        ).select_related ("parcel_owner")


class WithDrawParcel (generics.UpdateAPIView):
    queryset=Parcel.objects.select_related ("parcel_owner")
    permission_classes=(IsAuthenticated, ParcelPermissions)
    serializer_class=ParcelSerializer

    __doc__="""
    PATCH: This api is used to withdraw the package only parcel owner can withdraw it.
        params:
           withdraw_bids: BooleanField(True)

    """


class ParcelShippedDetailView (APIView):
    permission_classes=(IsAuthenticated, ParcelPermissions)

    __doc__="""
    GET: This api is used to tell the user that there parcel is shipped or not if shipped so it will return the cost of shipping
        Params:
            Parcel_id 
    """

    def get(self, request, *args, **kwargs):
        parcel=(
            Parcel.objects.filter (id=self.kwargs.get ("pk"))
            .annotate (cost=F ("shipped_parcel__train__cost"))
            .first ()
        )
        response_data=get_parcel_shipped_data (parcel)
        return Response (response_data, status=status.HTTP_200_OK)


class PostTrainOfferView (generics.ListCreateAPIView):
    queryset=Train.objects.select_related ("train_operator")
    permission_classes=(IsAuthenticated, TrainPermissions)
    serializer_class=PostTrainOfferSerializer
    pagination_class=LimitOffsetPagination

    __doc__="""
    GET: This api is used to return the list of all the posted offer train only post master and the train owner can access this api.
    POST: This api is used to post a train offer only train operator can access this api.
         Params:
            train_name: CharField
            capacity: DecimalField
            cost: DecimalField,
            lines_they_operate: ID's of the train track that they can operate
    """

    def perform_create(self, serializer):
        serializer.save (train_operator=self.request.user)

    def get_queryset(self):
        if self.request.user.user_type == "POST_MASTER":
            return self.queryset.filter (
                withdraw_bids=False, shipped_train=None
            ).select_related ("train_operator")
        return self.queryset.filter (
            train_operator=self.request.user, withdraw_bids=False, shipped_train=None
        ).select_related ("train_operator")


class WithDrawTrainOfferView (generics.UpdateAPIView):
    queryset=Train.objects.all ()
    permission_classes=(IsAuthenticated, TrainPermissions)
    serializer_class=PostTrainOfferSerializer

    __doc__="""
    PATCH: This api is used to withdraw the package only train operator can withdraw it.
       params:
           withdraw_bids: BooleanField(True)
    """


class TrainShippedDetailView (APIView):
    permission_classes=(IsAuthenticated, TrainPermissions)

    __doc__="""
    GET: This api is used to tell the user that there parcel is shipped or not if shipped so it will assigned lines, parcel detail and the train left time.
        Params:
            Train_id 
    """

    def get(self, request, *args, **kwargs):
        train=(
            Train.objects.filter (id=self.kwargs.get ("pk"))
            .annotate (
                parcel=F ("shipped_train__parcel"),
                train_left_time=F ("shipped_train__created"),
                assigned_lines=F ("shipped_train__assigned_lines"),
            )
            .first ()
        )
        response_data=get_train_shipped_data (train)
        return Response (response_data, status=status.HTTP_200_OK)


class TrainTrackView (generics.ListCreateAPIView):
    queryset=TrainTrack.objects.all ()
    permission_classes=(IsAuthenticated, PostMasterPermissions)
    serializer_class=TrainTrackSerializer
    pagination_class=LimitOffsetPagination

    __doc__="""
    GET: This api is used to return the list of all the train tracks only post master can access this api.
    POST: This api is used to create a train tracks only post master can access this api.
         Params:
            source: CharField
            destination: CharField
    """


class BookedTrainListView (generics.ListAPIView):
    queryset=ShippedParcel.objects.prefetch_related (
        "train", "parcel", "assigned_lines"
    )
    permission_classes=(IsAuthenticated, PostMasterPermissions)
    serializer_class=BookedTrainListSerializer
    pagination_class=LimitOffsetPagination

    __doc__="""
    GET: This api is used to return the list of all shipped train only post master have access to see this list.
    """


class BookTrainAndShippedView (generics.CreateAPIView):
    permission_classes=(IsAuthenticated, PostMasterPermissions)
    serializer_class=BookTrainAndShippedSerializer

    __doc__="""
        POST: This api is used to book a train and shipped the parcel only post master can book and send the train.
          Params:
              train_id: ID of the train,
              parcel_id: ID of the parcel,
              assigned_lines: ID of the lines that need to assign
    """