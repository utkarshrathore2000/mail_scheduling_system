from django.db.models import F
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Parcel, Train
from .permissions import ParcelPermissions, TrainPermissions
from .serializers import ParcelSerializer
from .utils import get_parcel_shipped_data


class ParcelView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, ParcelPermissions)
    serializer_class = ParcelSerializer
    queryset = Parcel.objects.all().select_related("parcel_owner")
    __doc__ = """
    GET: This api is used to return the list of all parcel list of the logged in parcel owner only parcel owner or post master can access this api.
    POST: This api is used to create a new parcel for ship only parcel owner user can access this api.
        params:
           parcel_name: CharField,
           parcel_weight: DecimalField,
           parcel_volume: DecimalField
    """

    def perform_create(self, serializer):
        serializer.save(parcel_owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(
            parcel_owner=self.request.user, withdraw_bids=False, shipped_parcel=None
        ).select_realted("parcel_owner")


class WithDrawParcel(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated, ParcelPermissions)
    serializer_class = ParcelSerializer
    queryset = Parcel.objects.all().select_related("parcel_owner")
    __doc__ = """
    PATCH: This api is used to withdraw the package only parcel owner can withdraw it.
        params:
           withdraw_bids: BooleanField(True)

    """


class ParcelShippedDetailView(APIView):
    permission_classes = (IsAuthenticated, ParcelPermissions)
    __doc__ = """
    GET: This api is used to tell the user that there parcel is shipped or not if shipped so it will return the cost of shipping
        Params:
            Parcel_id 
    """

    def get(self, request, *args, **kwargs):
        parcel = (
            Parcel.objects.filter(id=self.kwargs.get("pk"))
            .annotate(cost=F("shipped_parcel__train__cost"))
            .first()
        )
        response_data = get_parcel_shipped_data(parcel)
        return Response(response_data, status=status.HTTP_200_OK)


class PostTrainOfferView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, TrainPermissions)
    serializer_class = PostTrainOfferSerializer
    queryset = Train.objects.all().select_related("train_operator")
    __doc__ = """
    GET: This api is used to return the list of all the posted offer train only post master and the train owner can access this api.
    POST: This api is used to post a train offer only train operator can access this api.
         Params:
            train_name: CharField
            capacity: DecimalField
            cost: DecimalField,
            lines_they_operate: ID's of the train track that they can operate
    """

    def perform_create(self, serializer):
        serializer.save(train_operator=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(
            train_operator=self.request.user, withdraw_bids=False, shipped_train=None
        ).select_realted("train_operator")


class WithDrawTrainOfferView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated, TrainPermissions)
    serializer_class = PostTrainOfferSerializer
    queryset = Train.objects.all()
    __doc__ = """
    PATCH: This api is used to withdraw the package only train operator can withdraw it.
       params:
           withdraw_bids: BooleanField(True)
    """


class TrainShippedDetailView(APIView):
    permission_classes = (IsAuthenticated, TrainPermissions)
    __doc__ = """
    GET: This api is used to tell the user that there parcel is shipped or not if shipped so it will assigned lines, parcel detail and the train left time.
        Params:
            Train_id 
    """

    def get(self, request, *args, **kwargs):
        train = (
            Train.objects.filter(id=self.kwargs.get("pk"))
            .annotate(
                parcel=F("shipped_train__parcel"),
                train_left_time=F("shipped_train__created"),
                assigned_lines=F("shipped_train__assigned_lines"),
            )
            .first()
        )
        response_data = get_train_shipped_data(train)
        return Response(response_data, status=status.HTTP_200_OK)
