from django.conf import settings
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework.exceptions import NotAuthenticated


def get_user_id(request) -> dict:
    """
    To fetch the user id from the JWT Token in the request header by decoding it
    and return the user id in the dict.

    params: rest_framework.request.Request
    returns: dict containing user_id
    """

    message = {
        "detail": "Given token not valid for any token type",
        "code": "token_not_valid",
        "messages": [
            {
                "token_class": "AccessToken",
                "token_type": "access",
                "message": "Token is invalid or expired",
            }
        ],
    }

    auth_details = request.META.get("HTTP_AUTHORIZATION", " ").split(" ")
    if auth_details[0] == "Bearer":
        token = auth_details[1]
        try:
            valid_data = TokenBackend(
                algorithm=settings.SIMPLE_JWT["ALGORITHM"]
            ).decode(token, verify=False)

            user_id = valid_data["user_id"]
            return {"user_id": user_id}
        except:
            raise NotAuthenticated(message)

    elif auth_details[0] == "Basic":
        try:
            return {"user_id": request.user}
        except:
            raise NotAuthenticated(message)

    else:
        raise NotAuthenticated(message)
