from django.conf import settings
from rest_framework import permissions
from commons.scripts.get_user_id import get_user_id
from django.shortcuts import get_object_or_404
from market_garden.cropmap.models.section import Section


class IsSectionOwner(permissions.BasePermission):
    """
    Object-level permission to only allow owner of market-garden to edit
    its objects.
    """

    message = "You must be the owner of this MarketGarden's object."

    def has_object_permission(self, request, view, obj):
        data = get_user_id(request)
        return obj.section.market_garden.user_id == data["user_id"]


class IsValidSection(permissions.BasePermission):
    """
    Object-level permission to only allow owners of the market garden to edit
    its objects.
    """

    def has_object_permission(self, request, view, obj, **kwargs):
        return obj.market_garden.id == view.kwargs["pk_mk"]


class IsValidBed(permissions.BasePermission):
    """
    Object-level permission to only allow owners of the market garden to edit
    its objects.
    """

    def has_object_permission(self, request, view, obj, **kwargs):
        section = get_object_or_404(Section, pk=view.kwargs["pk_sec"])
        if section.market_garden.id == view.kwargs["pk_mk"]:
            return obj.section.id == view.kwargs["pk_sec"]
        else:
            return False
