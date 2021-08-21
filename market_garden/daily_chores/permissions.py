from rest_framework import permissions
from commons.scripts.get_user_id import get_user_id


class IsSpecific(permissions.BasePermission):
    """
    Object-level permission to only allow creators of an object to edit it.
    """

    message = "You must be the owner of this object."

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            data = get_user_id(request)
            return (
                obj.is_specific
                and obj.market_garden.filter(user=data["user_id"]).count() == 1
            )
