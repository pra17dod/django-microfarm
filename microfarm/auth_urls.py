from django.urls import path, include
from .auth_views import *
from dj_rest_auth.registration.views import (
    SocialAccountListView,
    SocialAccountDisconnectView,
)

urlpatterns = [
    path(r"", include("dj_rest_auth.urls")),
    path(r"registration/", include("dj_rest_auth.registration.urls")),
    path(r"facebook/", FacebookLogin.as_view(), name="fb_login"),
    path(r"google/", GoogleLogin.as_view(), name="google_login"),
    path(r"twitter/", TwitterLogin.as_view(), name="twitter_login"),
    path(r"facebook/connect/", FacebookConnect.as_view(), name="fb_connect"),
    path(r"google/connect/", GoogleConnect.as_view(), name="google_connect"),
    path(r"twitter/connect/", TwitterConnect.as_view(), name="twitter_connect"),
    path(
        r"socialaccounts/",
        SocialAccountListView.as_view(),
        name="social_account_list",
    ),
    path(
        r"socialaccounts/<int:pk>/disconnect/",
        SocialAccountDisconnectView.as_view(),
        name="social_account_disconnect",
    ),
]
