from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from commons.scripts.get_user_id import get_user_id


class IsOwner(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    """

    message = "You must be the owner of this object."

    def has_object_permission(self, request, view, obj):
        data = get_user_id(request)
        return obj.user_id == data["user_id"]


class IsMarketGardenOwner(permissions.BasePermission):
    """
    Object-level permission to only allow owners of the market garden to edit
    its objects.
    """

    message = "You must be the owner of this MarketGarden."

    def has_object_permission(self, request, view, obj):
        data = get_user_id(request)
        return obj.market_garden.user_id == data["user_id"]
