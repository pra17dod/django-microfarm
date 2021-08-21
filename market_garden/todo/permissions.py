from rest_framework import permissions


class IsValidTodo(permissions.BasePermission):
    """
    Object-level permission to only allow owners of the market garden to edit
    its objects.
    """

    def has_object_permission(self, request, view, obj, **kwargs):
        return obj.market_garden.id == view.kwargs["pk_mk"]
