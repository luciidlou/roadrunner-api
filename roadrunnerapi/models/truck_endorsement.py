from django.db import models


class TruckEndorsement(models.Model):
    truck = models.ForeignKey("Truck", on_delete=models.CASCADE)
    endorsement = models.ForeignKey("Endorsement", on_delete=models.CASCADE)
