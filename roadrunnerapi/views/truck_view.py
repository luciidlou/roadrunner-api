from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from roadrunnerapi.models import AppUser, Bid, Truck, Load


# -------------------- SERIALIZERS --------------------

class TruckSerializerGet(serializers.ModelSerializer):

    class Meta:
        model = Truck
        fields = ('id', 'alias', 'trailer_type', 'dispatcher',
                  'current_city', 'current_state', 'is_assigned',
                  'current_load')
        depth = 1
        
class LoadSerializerGet(serializers.ModelSerializer):

    class Meta:
        model = Load
        fields = ('id', 'distributor', 'created_on', 'pickup_address', 'pickup_city',
                  'pickup_state', 'pickup_datetime', 'dropoff_address', 'dropoff_city',
                  'dropoff_state', 'dropoff_datetime', 'distance', 'is_hazardous',
                  'is_booked', 'load_status', 'assigned_truck', 'freight_types', 'is_owner')
        depth = 2

# -----------------------------------------------------


class TruckView(ViewSet):
    def list(self, request):
        """Retrives all of the trucks that belong to the current user (current user must be a dispatcher)"""
        app_user = AppUser.objects.get(user=request.auth.user)

        if app_user.user_type == 'dispatcher':
            trucks = Truck.objects.filter(dispatcher=app_user)

            for truck in trucks:
                if truck.is_assigned:
                    bids = Bid.objects.filter(truck=truck, is_accepted=True)
                    loads = Load.objects.all()
                    for bid in bids:
                        for load in loads:
                            if bid.load_id == load.id:
                                found_load = Load.objects.get(pk=load.id)
                                serializer = LoadSerializerGet(found_load)
                                truck.current_load = serializer.data
                                break
                else:
                    truck.current_load = None

            serializer = TruckSerializerGet(trucks, many=True)

            return Response(serializer.data)
        else:
            return Response(
                {'message': 'Distributors do not have access to the fleet manager'}
            )
            