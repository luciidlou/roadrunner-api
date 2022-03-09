from django.db import models


class Bid(models.Model):
    load = models.ForeignKey("Load", on_delete=models.CASCADE)
    truck = models.ForeignKey("Truck", on_delete=models.CASCADE)
    dispatcher = models.ForeignKey("Dispatcher", on_delete=models.CASCADE)
    dollar_amount = models.FloatField()
    is_accepted = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
