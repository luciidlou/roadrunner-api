from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from roadrunnerapi.models import AppUser, Load, Bid

# -------------------- SERIALIZERS --------------------

class LoadSerializerGet(serializers.ModelSerializer):

    class Meta:
        model = Load
        fields = ('id', 'distributor', 'created_on', 'pickup_address', 'pickup_city',
                  'pickup_state', 'pickup_datetime', 'dropoff_address', 'dropoff_city',
                  'dropoff_state', 'dropoff_datetime', 'distance', 'is_hazardous',
                  'is_booked', 'load_status', 'assigned_truck')
        depth = 2

# -----------------------------------------------------

class LoadView(ViewSet):
    def list(self, request):
        """Retrives all of the unbooked loads"""
        loads = Load.objects.all()
        serializer = LoadSerializerGet(loads, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        """Retrives a single load"""
        load = Load.objects.get(pk=pk)
        serializer = LoadSerializerGet(load)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def booked(self, request):
        """Retrieves all of the booked loads that the current user is responsible for"""
        dispatcher_loads = []
        app_user = AppUser.objects.get(user_id=request.auth.user_id)
        if app_user.user_type == "distributor":
            distributor_loads = Load.objects.filter(
                distributor=app_user, is_booked=True)
            serializer = LoadSerializerGet(distributor_loads, many=True)
            return Response(serializer.data)
        else:
            loads = Load.objects.all()
            bids = Bid.objects.filter(is_accepted=True, dispatcher=app_user)
            for load in loads:
                for bid in bids:
                    if load == bid.load:
                        dispatcher_loads.append(load)
            serializer = LoadSerializerGet(dispatcher_loads, many=True)
            return Response(serializer.data)