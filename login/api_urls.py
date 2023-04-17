from django.urls import path
from login.views import (
    CitySubScribe,
)

app_name = 'api'

urlpatterns = [
    path('add_city', CitySubScribe.as_view(), name='citypost'),
]