from django.urls import path # type: ignore
from . import views

urlpatterns = [
    path('api/rooms/', views.room_list, name='room-list'),
]
