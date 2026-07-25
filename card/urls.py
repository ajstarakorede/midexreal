from django.urls import path

from . import views

urlpatterns = [
    path("", views.card_view, name="card"),
]
