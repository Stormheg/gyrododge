from django.contrib import admin
from gyrododge.score.models import Score


# Registreer Score model zodat deze in de admin interface zichtbaar wordt.
@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ["name", "points", "date_added"]
    ordering = ("-points", "-date_added")
