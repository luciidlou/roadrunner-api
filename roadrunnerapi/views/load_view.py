from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
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
                  'is_booked', 'load_status', 'assigned_truck', 'freight_types')
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
        loads = Load.objects.all()
        serializer = LoadSerializerGet(loads, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        """Retrives a single load"""
        load = Load.objects.get(pk=pk)
        serializer = LoadSerializerGet(load)
        return Response(serializer.data)

    def create(self, request):
        """Creates a new Load object"""
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
