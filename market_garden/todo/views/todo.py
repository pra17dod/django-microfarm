from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from django.shortcuts import get_object_or_404
from commons.scripts.get_user_id import get_user_id
from commons.permissions import IsMarketGardenOwner
from market_garden.todo.permissions import IsValidTodo
from market_garden.cropmap.models.cropmap import MarketGarden
from market_garden.todo.models.todo_daily_chores import (
    TodoDailyChores,
    TodoDailyChoresSerializer,
)
from market_garden.todo.models.todo_mulching import TodoMulching, TodoMulchingSerializer
from market_garden.todo.models.todo_watering import TodoWatering, TodoWateringSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


class TodoListView(APIView):
    def get(self, request, pk=None, format=None):
        data = get_user_id(self.request)
        if get_object_or_404(MarketGarden, user_id=data["user_id"], pk=pk):
            daily_chores = TodoDailyChores.objects.filter(market_garden_id=pk)
            mulching = TodoMulching.objects.filter(market_garden_id=pk)
            watering = TodoWatering.objects.filter(market_garden_id=pk)

            daily_chores_serializer = TodoDailyChoresSerializer(daily_chores, many=True)
            mulching_serializer = TodoMulchingSerializer(mulching, many=True)
            watering_serializer = TodoWateringSerializer(watering, many=True)

            data = {
                "daily_chores": daily_chores_serializer.data,
                "mulching": mulching_serializer.data,
                "watering": watering_serializer.data,
            }

            return Response(data)

        else:
            return NotFound


class TodoDailyChoresListView(ListCreateAPIView):
    queryset = TodoDailyChores.objects.all()
    serializer_class = TodoDailyChoresSerializer

    def get_queryset(self, **kwargs):
        """
        This view should return a list of all Todo DailyChores for the currently
        authenticated user's market-garden.
        """
        user_id = get_user_id(self.request)["user_id"]
        market_garden = get_object_or_404(MarketGarden, pk=self.kwargs["pk_mk"])
        if market_garden.user_id == user_id:
            todos = TodoDailyChores.objects.filter(market_garden=market_garden)
            if todos:
                return todos
            else:
                raise NotFound
        else:
            raise PermissionDenied


class TodoDailyChoresDetailView(RetrieveUpdateDestroyAPIView):
    queryset = TodoDailyChores.objects.all()
    serializer_class = TodoDailyChoresSerializer
    permission_classes = [IsValidTodo, IsMarketGardenOwner]


class TodoMulchingListView(ListCreateAPIView):
    queryset = TodoMulching.objects.all()
    serializer_class = TodoMulchingSerializer

    def get_queryset(self, **kwargs):
        """
        This view should return a list of all Todo Mulching for the currently
        authenticated user's market-garden.
        """
        user_id = get_user_id(self.request)["user_id"]
        market_garden = get_object_or_404(MarketGarden, pk=self.kwargs["pk_mk"])
        if market_garden.user_id == user_id:
            todos = TodoMulching.objects.filter(market_garden=market_garden)
            if todos:
                return todos
            else:
                raise NotFound
        else:
            raise PermissionDenied


class TodoMulchingDetailView(RetrieveUpdateDestroyAPIView):
    queryset = TodoMulching.objects.all()
    serializer_class = TodoMulchingSerializer
    permission_classes = [IsValidTodo, IsMarketGardenOwner]


class TodoWateringListView(ListCreateAPIView):
    queryset = TodoWatering.objects.all()
    serializer_class = TodoWateringSerializer

    def get_queryset(self, **kwargs):
        """
        This view should return a list of all Todo Watering for the currently
        authenticated user's market-garden.
        """
        user_id = get_user_id(self.request)["user_id"]
        market_garden = get_object_or_404(MarketGarden, pk=self.kwargs["pk_mk"])
        if market_garden.user_id == user_id:
            todos = TodoWatering.objects.filter(market_garden=market_garden)
            if todos:
                return todos
            else:
                raise NotFound
        else:
            raise PermissionDenied


class TodoWateringDetailView(RetrieveUpdateDestroyAPIView):
    queryset = TodoWatering.objects.all()
    serializer_class = TodoWateringSerializer
    permission_classes = [IsValidTodo, IsMarketGardenOwner]
