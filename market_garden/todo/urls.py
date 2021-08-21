from django.urls import path
from market_garden.todo.views.todo import (
    TodoListView,
    TodoDailyChoresListView,
    TodoDailyChoresDetailView,
    TodoMulchingListView,
    TodoMulchingDetailView,
    TodoWateringListView,
    TodoWateringDetailView,
)

urlpatterns = [
    path(
        r"api/market/garden/<int:pk>/todo/",
        TodoListView.as_view(),
        name="market_garden-todo-list",
    ),
    path(
        r"api/market/garden/<int:pk_mk>/todo/daily/chores/",
        TodoDailyChoresListView.as_view(),
        name="market_garden-todo-daily_chores-list",
    ),
    path(
        r"api/market/garden/<int:pk_mk>/todo/daily/chores/<int:pk>/",
        TodoDailyChoresDetailView.as_view(),
        name="market_garden-todo-daily_chores-detail",
    ),
    path(
        r"api/market/garden/<int:pk_mk>/todo/mulching/",
        TodoMulchingListView.as_view(),
        name="market_garden-todo-mulching-list",
    ),
    path(
        r"api/market/garden/<int:pk_mk>/todo/mulching/<int:pk>/",
        TodoMulchingDetailView.as_view(),
        name="market_garden-todo-mulching-detail",
    ),
    path(
        r"api/market/garden/<int:pk_mk>/todo/watering/",
        TodoWateringListView.as_view(),
        name="market_garden-todo-watering-list",
    ),
    path(
        r"api/market/garden/<int:pk_mk>/todo/watering/<int:pk>/",
        TodoWateringDetailView.as_view(),
        name="market_garden-todo-watering-detail",
    ),
]
