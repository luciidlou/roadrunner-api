from datetime import timedelta
from django.db import models
from django.db.models import Max, Min, Avg
from rest_framework import serializers
from roadrunnerapi.models.bid import Bid
from roadrunnerapi.models.truck import Truck


class Load(models.Model):
    """Model for a Load object"""
    distributor = models.ForeignKey("AppUser", on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    pickup_address = models.CharField(max_length=300)
    pickup_city = models.CharField(max_length=300)
    pickup_state = models.CharField(max_length=2)
    pickup_datetime = models.DateTimeField()
    dropoff_address = models.CharField(max_length=300)
    dropoff_city = models.CharField(max_length=300)
    dropoff_state = models.CharField(max_length=2)
    dropoff_datetime = models.DateTimeField()
    distance = models.PositiveIntegerField()
    is_hazardous = models.BooleanField(default=False)
    is_booked = models.BooleanField(default=False)
    load_status = models.ForeignKey(
        "LoadStatus", on_delete=models.CASCADE, null=True)
    freight_types = models.ManyToManyField(
        "FreightType", through="LoadFreightType", related_name="freight_types")

    @property
    def assigned_truck(self):
        """Returns the assigned truck on booked loads"""
        try:
            bid = Bid.objects.get(is_accepted=True, load=self)
            truck = Truck.objects.get(pk=bid.truck_id)
            serializer = TruckSerializerGet(truck)
            return serializer.data
        except Bid.DoesNotExist:
            return None

    @property
    def is_owner(self):
        """Checks to see if the load is owned by the current user. Returns boolean"""
        return self.__is_owner

    @is_owner.setter
    def is_owner(self, value):
        self.__is_owner = value

    @property
    def bid_macros(self):
        "Returns the highest on a load"
        bids = Bid.objects.filter(load=self)
        macros = Bid.objects.filter(load=self).aggregate(
            Max('dollar_amount'), Min('dollar_amount'), Avg('dollar_amount'))
        if len(bids) > 0:
            return {
                'count': len(bids),
                'avg': round(macros['dollar_amount__avg'], 2),
                'max': round(macros['dollar_amount__max'], 2),
                'min': round(macros['dollar_amount__min'], 2)
            }
        else:
            return {
                'count': 0,
                'avg': 0,
                'max': 0,
                'min': 0
            }

    @property
    def bid_ending(self):
        """Returns a datetime value that is exactly 24hours before pickup_datetime property"""
        time_delta = timedelta(hours=19)
        return self.pickup_datetime - time_delta

# -------------------- SERIALIZERS --------------------


class TruckSerializerGet(serializers.ModelSerializer):

    class Meta:
        model = Truck
        fields = ('id', 'alias', 'trailer_type', 'dispatcher',
                  'current_city', 'current_state', 'is_assigned')
        depth = 1

# -----------------------------------------------------
