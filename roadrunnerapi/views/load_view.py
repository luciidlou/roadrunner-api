from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from django.utils.timezone import make_naive
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from roadrunnerapi.models import AppUser, Bid, Load, LoadFreightType
from roadrunnerapi.models.freight_type import FreightType

# -------------------- SERIALIZERS --------------------


class LoadSerializerGet(serializers.ModelSerializer):

    class Meta:
        model = Load
        fields = ('id', 'distributor', 'created_on', 'pickup_address', 'pickup_city',
                  'pickup_state', 'pickup_datetime', 'dropoff_address', 'dropoff_city',
                  'dropoff_state', 'dropoff_datetime', 'distance', 'is_hazardous',
                  'is_booked', 'load_status', 'assigned_truck', 'freight_types', 'is_owner')
        depth = 2


class LoadSerializerCreate(serializers.ModelSerializer):

    class Meta:
        model = Load
        fields = ('pickup_address', 'pickup_city', 'pickup_state', 'pickup_datetime',
                  'dropoff_address', 'dropoff_city', 'dropoff_state', 'dropoff_datetime',
                  'distance', 'is_hazardous', 'freight_types')
        depth = 2

# -----------------------------------------------------


class LoadView(ViewSet):
    def list(self, request):
        """Retrives all of the unbooked loads"""
        app_user = AppUser.objects.get(user=request.auth.user)
        loads = Load.objects.all()

        for load in loads:
            if load.distributor == app_user:
                load.is_owner = True
            else:
                load.is_owner = False

        serializer = LoadSerializerGet(loads, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        """Retrives a single load"""
        app_user = AppUser.objects.get(user=request.auth.user)
        load = Load.objects.get(pk=pk)

        if load.distributor == app_user:
            load.is_owner = True
        else:
            load.is_owner = False

        serializer = LoadSerializerGet(load)
        return Response(serializer.data)

    def create(self, request):
        """Creates a new Load object (POST request)"""
        distributor = AppUser.objects.get(user=request.auth.user)
        freight_types_list = []

        for freight_type_id in request.data['freight_types']:
            freight_type = FreightType.objects.get(pk=freight_type_id)
            freight_types_list.append(freight_type)

        serializer = LoadSerializerCreate(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_load = serializer.save(distributor=distributor)

        new_load.freight_types.set(freight_types_list)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Updates an existing Load object (PUT request)"""
        load = Load.objects.get(pk=pk)
        freight_types_list = []

        load.pickup_address = request.data['pickup_address']
        load.pickup_city = request.data['pickup_city']
        load.pickup_state = request.data['pickup_state']
        load.pickup_datetime = request.data['pickup_datetime']
        load.dropoff_address = request.data['dropoff_address']
        load.dropoff_city = request.data['dropoff_city']
        load.dropoff_state = request.data['dropoff_state']
        load.dropoff_datetime = request.data['dropoff_datetime']
        load.distance = request.data['distance']
        load.is_hazardous = request.data['is_hazardous']
        for freight_type_id in request.data['freight_types']:
            freight_type = FreightType.objects.get(pk=freight_type_id)
            freight_types_list.append(freight_type)

        load.freight_types.set(freight_types_list)
        load.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

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
