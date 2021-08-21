from django.db import models
from rest_framework import serializers
from django.conf import settings
from commons.models.rule import RuleModel
from commons.models.task import TaskModel


class MulchingRule(TaskModel):
    bed_new = models.BooleanField(
        verbose_name="If Bed New then mulching?",
        default=True,
        editable=True,
    )

    class Meta:
        verbose_name_plural = "05 Mulching Rules"

    def __str__(self):
        return str(self.name)


class MulchingRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = MulchingRule
        fields = "__all__"


class CustomMulchingRule(RuleModel):
    parent_rule = models.ForeignKey(
        MulchingRule,
        verbose_name="Custom Rule",
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.parent_rule.name} - {self.name}"


class CustomMulchingRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomMulchingRule
        fields = "__all__"
