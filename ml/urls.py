from django.urls import path,include
from .views import IrisPredictionAPI
urlpatterns = [
    path('',IrisPredictionAPI.as_view()),
]
