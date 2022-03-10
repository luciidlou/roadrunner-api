from django.db import models


class Load(models.Model):
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
    load_status = models.ForeignKey("LoadStatus", on_delete=models.CASCADE, null=True)
    freight_types = models.ManyToManyField(
        "FreightType", through="LoadFreightType", related_name="freight_types")
