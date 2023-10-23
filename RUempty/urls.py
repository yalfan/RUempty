
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("update_db", views.update_db, name="update_db"),
    path("buildings/<str:campus>", views.get_buildings, name="buildings"),
    path("rooms", views.rooms, name="rooms"),
]
