from rest_framework import serializers


class SubscribeSerializer(serializers.Serializer):
    SUBSCRIBE_TYPE_CHOICES = (("SU", "Наш кинотеатр"), ("AM", "Амедиатека"))
    subscribe_type = serializers.ChoiceField(
        choices=SUBSCRIBE_TYPE_CHOICES, required=True
    )


class WebhookSerializer(serializers.Serializer):
    type = serializers.CharField(required=True)
    data = serializers.JSONField(required=True)
