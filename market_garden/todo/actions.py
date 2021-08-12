from django.contrib import admin, messages


def success_message(request, status):
    messages.success(request, f"Selected Record(s) Marked as {status} Successfully !!")


def action_description(action, status):
    action.short_description = f"Mark selected Record(s) as {status}"


def mark_upcoming(modeladmin, request, queryset):
    queryset.update(status=3)
    success_message(request, "Upcoming")


action_description(mark_upcoming, "Upcoming")


def mark_started(modeladmin, request, queryset):
    queryset.update(status=2)
    success_message(request, "Started")


action_description(mark_started, "Started")


def mark_paused(modeladmin, request, queryset):
    queryset.update(status=1)
    success_message(request, "Paused")


action_description(mark_paused, "Paused")


def mark_completed(modeladmin, request, queryset):
    queryset.update(status=0)
    success_message(request, "Completed")


action_description(mark_completed, "Completed")


def mark_expired(modeladmin, request, queryset):
    queryset.update(status=-1)
    success_message(request, "Expired")


action_description(mark_expired, "Expired")
