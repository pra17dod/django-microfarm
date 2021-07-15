from django.contrib import admin
from market_garden.cropmap.models.cropmap import MarketGarden
from market_garden.cropmap.models.section import Section, Bed
from market_garden.daily_chores.models.daily_chores import DailyChores
from market_garden.watering.models.watering import WateringRule
from market_garden.mulching.models.mulching import MulchingRule, CustomMulchingRule


@admin.register(MarketGarden)
class MarketGardenAdmin(admin.ModelAdmin):

    fieldsets = [
        (
            "User Details",
            {
                "fields": [
                    "user",
                    "latitude",
                    "longitude",
                    "length",
                    "width",
                ]
            },
        ),
        (
            "Crop Map Contraints",
            {
                "fields": [
                    "path_width",
                    "path_width_btw_sections",
                    "min_bed_length",
                    "max_bed_length",
                    "min_bed_per_section",
                    "max_bed_per_section",
                ]
            },
        ),
        (
            "Crop Map Parameters",
            {
                "fields": [
                    "bed_length",
                    "bed_width",
                    "bed_along_side_name",
                    "num_of_bed_along_side",
                    "num_of_bed_along_otherside",
                    "bed_per_section",
                    "total_sections",
                    "area_used",
                ]
            },
        ),
        (
            "Compost Requirements",
            {
                "fields": [
                    "compost_height_of_bed",
                    "compost_height_of_path",
                    "compost_required_per_bed",
                    "total_compost_required",
                ]
            },
        ),
        (
            "Important Dates",
            {
                "fields": [
                    "created_at",
                    "updated_at",
                ]
            },
        ),
    ]
    readonly_fields = [
        "updated_at",
        "created_at",
    ]
    list_display = (
        "user",
        "created_at",
    )
    list_filter = ["user"]


class BedAdmin(admin.StackedInline):
    model = Bed


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    inlines = [BedAdmin]
    list_filter = ["user"]

    class Meta:
        model = Section


@admin.register(DailyChores)
class DailyChoresAdmin(admin.ModelAdmin):
    pass


class CustomMulchingRuleAdmin(admin.StackedInline):
    model = CustomMulchingRule


@admin.register(MulchingRule)
class MulchingRuleAdmin(admin.ModelAdmin):
    inlines = [CustomMulchingRuleAdmin]

    class Meta:
        model = MulchingRule


@admin.register(WateringRule)
class WateringRuleAdmin(admin.ModelAdmin):
    pass
