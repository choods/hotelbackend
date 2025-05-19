from django.http import JsonResponse
from rest_framework import viewsets, permissions
from rooms.models import Room
from .models import Reservation
from .serializers import ReservationSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import datetime

class CheckRoomAvailability(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        check_in = request.GET.get('check_in')
        check_out = request.GET.get('check_out')

        # Check for missing date parameters
        if not check_in or not check_out:
            return Response({"error": "Check-in and check-out dates are required."}, status=400)

        # Convert dates to datetime objects
        try:
            check_in_date = timezone.datetime.strptime(check_in, '%Y-%m-%d').date()
            check_out_date = timezone.datetime.strptime(check_out, '%Y-%m-%d').date()
        except ValueError:
            return Response({"error": "Invalid date format."}, status=400)

        # Query for reservations that overlap the requested dates
        reserved_rooms = Reservation.objects.filter(
            check_in__lt=check_out_date,
            check_out__gt=check_in_date
        )

        # Create a list of room numbers from the filtered reservations
        unavailable_rooms = [reservation.room_numbers for reservation in reserved_rooms]

        return Response({
            'unavailable_rooms': unavailable_rooms
        })

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Extract room data from request
        room_name = self.request.data.get('room_name')
        room_price = self.request.data.get('room_price')
        room_id = self.request.data.get('room_id')

        # You can also do some validation here if necessary
        if not room_name or not room_price or not room_id:
            return Response(
                {"error": "Missing room data (name, price, or id)"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Pass the room data along with other validated data
        serializer.save(
            user=self.request.user,
            room_name=room_name,
            room_price=room_price,
            room_id=room_id
        )

@api_view(['POST'])
def cancel_reservation(request):
    print("Incoming data:", request.data)
    reservation_id = request.data.get('reservation_id')
    if not reservation_id:
        return Response({"error": "Reservation ID is required."}, status=400)

    try:
        reservation = Reservation.objects.get(id=reservation_id, user=request.user)
        reservation.delete()
        return Response({"message": "Reservation cancelled successfully"})
    except Reservation.DoesNotExist:
        return Response({"error": "Reservation not found"}, status=404)

def cancel_room(request, room_number):
    # Find the room and update its status to available
    room = Room.objects.get(room_number=room_number)
    room.status = 'available'
    room.save()
    return JsonResponse({'status': 'success'})

class UnavailableRoomTypes(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Expect ?check_in=YYYY-MM-DD&check_out=YYYY-MM-DD
        ci = request.GET.get("check_in")
        co = request.GET.get("check_out")
        if not ci or not co:
            return Response({"error":"Missing dates"}, status=400)

        try:
            check_in = parse_date(ci)
            check_out = parse_date(co)
        except:
            return Response({"error":"Bad date format"}, status=400)

        # Overlapping reservations
        qs = Reservation.objects.filter(
            check_in__lt=check_out,
            check_out__gt=check_in
        )
        # Extract distinct room_name values
        types = qs.values_list("room_name", flat=True).distinct()
        return Response({"unavailable_types": list(types)})