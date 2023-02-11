from django.urls import path

from .views import ParcelView, WithDrawParcel, ParcelShippedDetailView

urlpatterns = [
    # Parcel related endpoints
    path("post-parcel/", ParcelView.as_view()),
    path("withdraw-parcel/<int:pk>/", WithDrawParcel.as_view()),
    path("parcel-shipped-detail/<int:pk>/", ParcelShippedDetailView.as_view()),
]
