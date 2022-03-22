from datetime import datetime

from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from roadrunnerapi.models import (AppUser, Bid, Endorsement, Load, TrailerType,
                                  Truck)

# -------------------- SERIALIZERS --------------------


class TruckSerializerGet(serializers.ModelSerializer):

    class Meta:
        model = Truck
        fields = ('id', 'alias', 'trailer_type', 'dispatcher',
                  'current_city', 'current_state', 'is_assigned',
                  'endorsements', 'current_load', 'is_active',
                  'created_on', 'retired_on')
        depth = 1


class TruckSerializerCreate(serializers.ModelSerializer):

    class Meta:
        model = Truck
        fields = ('alias', 'trailer_type', 'current_city',
                  'current_state', 'endorsements')


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

    def retrieve(self, request, pk):
        """Retrives a single Truck object"""
        truck = Truck.objects.get(pk=pk)

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

        serializer = TruckSerializerGet(truck)

        return Response(serializer.data)

    def create(self, request):
        """Creates a new Truck object (POST method)"""
        dispatcher = AppUser.objects.get(user=request.auth.user)
        trailer_type = TrailerType.objects.get(pk=request.data['trailer_type'])
        endorsements_list = []

        for endorsement_id in request.data['endorsements']:
            endorsement = Endorsement.objects.get(pk=endorsement_id)
            endorsements_list.append(endorsement)

        serializer = TruckSerializerCreate(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_truck = serializer.save(
            dispatcher=dispatcher, trailer_type=trailer_type)

        new_truck.endorsements.set(endorsements_list)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Updates an existing truck object (PUT request)"""
        truck = Truck.objects.get(pk=pk)
        trailer_type = TrailerType.objects.get(pk=request.data['trailer_type'])
        endorsements_list = []

        for endorsement_id in request.data['endorsements']:
            endorsement = Endorsement.objects.get(pk=endorsement_id)
            endorsements_list.append(endorsement)

        truck.alias = request.data['alias']
        truck.trailer_type = trailer_type
        truck.current_city = request.data['current_city']
        truck.current_state = request.data['current_state']
        truck.endorsements.set(endorsements_list)

        truck.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['put'], detail=True)
    def retire(self, request, pk):
        """Flips the value of a trucks is_active property (BOOLEAN)"""
        truck = Truck.objects.get(pk=pk)

        if truck.is_active is True:
            truck.is_active = False
            truck.retired_on = datetime.now()
        else:
            truck.is_active = True
            truck.retired_on = None

        truck.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
