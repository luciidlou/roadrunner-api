from django.db import models


class DispatcherRating(models.Model):
    distributor = models.ForeignKey("Distributor", on_delete=models.CASCADE)
    dispatcher = models.ForeignKey("Dispatcher", on_delete=models.CASCADE)
    Rating = models.PositiveSmallIntegerField(min=1, max=5)
