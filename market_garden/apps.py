from django.apps import AppConfig


class MarketGardenConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "market_garden"
    verbose_name = "Market Garden Database"

    def ready(self):
        import market_garden.cropmap.signals
        import market_garden.watering.signals
