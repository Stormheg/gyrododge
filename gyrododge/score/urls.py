from django.contrib.admindocs.urls import urlpatterns
from django.urls import path

from gyrododge.score.views import PostScoreApi

app_name = "score"

urlpatterns = [
    path("score/new/", PostScoreApi.as_view(), name="new")
]
