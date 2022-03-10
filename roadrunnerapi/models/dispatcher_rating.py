from django.db import models


class DispatcherRating(models.Model):
    distributor = models.ForeignKey("AppUser", on_delete=models.CASCADE, related_name="distributor")
    dispatcher = models.ForeignKey("AppUser", on_delete=models.CASCADE, related_name="dispatcher")
    Rating = models.PositiveSmallIntegerField()
