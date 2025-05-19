from django.urls import path
from .views import CheckRoomAvailability
from rest_framework.routers import DefaultRouter
from .views import ReservationViewSet
from .views import UnavailableRoomTypes

router = DefaultRouter()
router.register(r'api/reservations', ReservationViewSet)

urlpatterns = [
    # Add the correct path for the 'unavailable' check
    path('api/reservations/unavailable/', CheckRoomAvailability.as_view(), name='check_room_availability'),
    path(
      "api/reservations/unavailable-types/",
      UnavailableRoomTypes.as_view(),
      name="unavailable_room_types"
    ),
] + router.urls
