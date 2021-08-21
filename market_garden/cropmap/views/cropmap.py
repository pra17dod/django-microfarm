from rest_framework import viewsets
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied, NotFound
from commons.scripts.get_user_id import get_user_id
from commons.permissions import IsOwner, IsMarketGardenOwner
from market_garden.cropmap.permissions import IsSectionOwner, IsValidSection, IsValidBed
from market_garden.cropmap.models.cropmap import MarketGarden, MarketGardenSerializer
from market_garden.cropmap.models.section import (
    Bed,
    Section,
    BedSerializer,
    SectionSerializer,
)


class MarketGardenViewSet(viewsets.ModelViewSet):
    queryset = MarketGarden.objects.all()
    serializer_class = MarketGardenSerializer
    permission_classes = [IsOwner]

    def perform_create(self, serializer):
        """
        This view should assign the currently authenticated user as the owner of
        the market-garden created.
        """
        user_id = get_user_id(self.request)["user_id"]
        User = get_user_model()
        user = get_object_or_404(User, pk=user_id)
        serializer.save(user=user)

    def get_queryset(self):
        """
        This view should return a list of all market-gardens for the currently
        authenticated user.
        """
        user_id = get_user_id(self.request)["user_id"]
        market_gardens = MarketGarden.objects.filter(user_id=user_id)
        if market_gardens:
            return market_gardens
        else:
            raise NotFound


class SectionListView(ListCreateAPIView):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer

    def get_queryset(self, **kwargs):
        """
        This view should return a list of all sections for the currently
        authenticated user's market-garden.
        """
        user_id = get_user_id(self.request)["user_id"]
        market_garden = get_object_or_404(MarketGarden, pk=self.kwargs["pk_mk"])
        if market_garden.user_id == user_id:
            sections = Section.objects.filter(market_garden_id=market_garden.id)
            if sections:
                return sections
            else:
                raise NotFound
        else:
            raise PermissionDenied


class SectionDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = [IsValidSection, IsMarketGardenOwner]


class BedListView(ListCreateAPIView):
    queryset = Bed.objects.all()
    serializer_class = BedSerializer
    permission_classes = [IsValidSection, IsMarketGardenOwner]

    def get_queryset(self, **kwargs):
        """
        This view should return a list of all beds for the currently
        authenticated user's market-garden's section.
        """
        user_id = get_user_id(self.request)["user_id"]
        section = get_object_or_404(Section, pk=self.kwargs["pk_sec"])
        if section.market_garden.user_id == user_id:
            if section.market_garden.id == self.kwargs["pk_mk"]:
                return Bed.objects.filter(section_id=self.kwargs["pk_sec"])
            else:
                raise PermissionDenied
        else:
            raise PermissionDenied


class BedDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Bed.objects.all()
    serializer_class = BedSerializer
    permission_classes = [IsValidSection, IsValidBed, IsSectionOwner]
