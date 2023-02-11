from django.urls import path

from .views import (BookedTrainListView, BookTrainAndShippedView,
                    ParcelShippedDetailView, ParcelView, PostTrainOfferView,
                    TrainShippedDetailView, TrainTrackView, WithDrawParcel,
                    WithDrawTrainOfferView)

urlpatterns = [
    # Parcel related endpoints
    path("post-parcel/", ParcelView.as_view()),
    path("withdraw-parcel/<int:pk>/", WithDrawParcel.as_view()),
    path("parcel-shipped-detail/<int:pk>/", ParcelShippedDetailView.as_view()),
    # Train post offer related endpoints
    path("post-train-offer/", PostTrainOfferView.as_view()),
    path("withdraw-train-offer/<int:pk>/", WithDrawTrainOfferView.as_view()),
    path("train-shipped-detail/<int:pk>/", TrainShippedDetailView.as_view()),
    # Train track related endpoints
    path("train-tracks/", TrainTrackView.as_view()),
    # Booked train fill parcel and shipped train related endpoints
    path("booked-train-list/", BookedTrainListView.as_view()),
    path("book-train/", BookTrainAndShippedView.as_view()),
]
