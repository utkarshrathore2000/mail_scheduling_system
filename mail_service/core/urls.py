from django.conf.urls import url
from django.urls import include, path

from .views import SignUpApiView

urlpatterns = [
    path("sign-up/", SignUpApiView.as_view()),
]