from django.contrib import admin
from market_garden.todo.models.todo_daily_chores import TodoDailyChores
from market_garden.todo.models.todo_mulching import TodoMulching
from market_garden.todo.models.todo_watering import TodoWatering
from market_garden.todo.actions import (
    mark_upcoming,
    mark_started,
    mark_paused,
    mark_completed,
    mark_expired,
)


@admin.register(TodoDailyChores)
class TodoDailyChoresAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "daily_chores",
        "market_garden",
        "status",
        "updated_at",
        "created_at",
    ]
    list_filter = ["market_garden", "status"]
    actions = [
        mark_upcoming,
        mark_started,
        mark_paused,
        mark_completed,
        mark_expired,
    ]


@admin.register(TodoMulching)
class TodoMulchingAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "market_garden",
        "status",
        "updated_at",
        "created_at",
    ]
    list_filter = ["market_garden", "status"]
    actions = [
        mark_upcoming,
        mark_started,
        mark_paused,
        mark_completed,
        mark_expired,
    ]


@admin.register(TodoWatering)
class TodoWateringAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "market_garden",
        "status",
        "updated_at",
        "created_at",
    ]
    list_filter = ["market_garden", "status"]
    actions = [
        mark_upcoming,
        mark_started,
        mark_paused,
        mark_completed,
        mark_expired,
    ]
