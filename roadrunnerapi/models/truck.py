from django.db import models


class Truck(models.Model):
    alias = models.CharField(max_length=120)
    trailer_type = models.ForeignKey("TrailerType", on_delete=models.CASCADE)
    dispatcher = models.ForeignKey("Dispatcher", on_delete=models.CASCADE)
    current_city = models.CharField(max_length=300)
    current_state = models.CharField(max_length=30)
    is_assigned = models.BooleanField(default=False)
    endorsements = models.ManyToManyField("Endorsement", through="TruckEndorsement", related_name="endorsements")