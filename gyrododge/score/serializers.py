from rest_framework import serializers

from gyrododge.score.models import Score


class ScoreSerializer(serializers.ModelSerializer):
    """ScoreSerializer. Validates input"""

    class Meta:
        model = Score
        fields = ["points",]


class PositionSerializer(serializers.Serializer):
    """PositionSerializer. Serializes output"""
    position = serializers.IntegerField()
