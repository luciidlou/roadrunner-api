from django.db import models
from rest_framework import serializers, status
from rest_framework.response import Response
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


# -------------------- SERIALIZERS --------------------

class TruckSerializerGet(serializers.ModelSerializer):

    class Meta:
        model = Truck
        fields = ('id', 'alias', 'trailer_type', 'dispatcher',
                  'current_city', 'current_state', 'is_assigned')
        depth = 1

# -----------------------------------------------------
