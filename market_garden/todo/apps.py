from django.apps import AppConfig


class TodoConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "market_garden.todo"
    verbose_name = "Market Garden Todo"

    def ready(self):
        import market_garden.todo.signals
