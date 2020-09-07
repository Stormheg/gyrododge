from django.db import models


class Score(models.Model):
    """Score model"""

    points = models.PositiveIntegerField()
    date_added = models.DateTimeField(auto_now_add=True)

    def get_position(self) -> int:
        """Get position as int"""
        return Score.objects.filter(points__gt=self.points).count() + 1

    def __str__(self) -> str:
        return str(self.points)
