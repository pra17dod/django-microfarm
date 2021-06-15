from django.urls import path, include
from .auth_views import *
from dj_rest_auth.registration.views import (
    SocialAccountListView,
    SocialAccountDisconnectView,
)

urlpatterns = [
    path("", include("dj_rest_auth.urls")),
    path("registration/", include("dj_rest_auth.registration.urls")),
    path("facebook/", FacebookLogin.as_view(), name="fb_login"),
    path("google/", GoogleLogin.as_view(), name="google_login"),
    path("twitter/", TwitterLogin.as_view(), name="twitter_login"),
    path("facebook/connect/", FacebookConnect.as_view(), name="fb_connect"),
    path("google/connect/", GoogleConnect.as_view(), name="google_connect"),
    path("twitter/connect/", TwitterConnect.as_view(), name="twitter_connect"),
    path(
        "socialaccounts/", SocialAccountListView.as_view(), name="social_account_list"
    ),
    path(
        "socialaccounts/<int:pk>/disconnect/",
        SocialAccountDisconnectView.as_view(),
        name="social_account_disconnect",
    ),
]
