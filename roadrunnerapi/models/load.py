from django.db import models

class Load(models.Model):
    distributor = models.ForeignKey("Distributor", on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    pickup_city = models.CharField(max_length=300)
    pickup_state = models.CharField(max_length=30)
    pickup_datetime = models.DateTimeField()
    dropoff_city = models.CharField(max_length=300)
    dropoff_state = models.CharField(max_length=30)
    dropoff_datetime = models.DateTimeField()
    distance = models.PositiveIntegerField()
    is_hazardous = models.BooleanField()
    is_booked = models.BooleanField()
    load_status = models.ForeignKey("LoadStatus", on_delete=models.CASCADE)
    freight_types = models.ManyToManyField("FreightType", through="TruckEndorsement", related_name="endorsements")