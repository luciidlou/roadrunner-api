from django.db import models


class FreightType(models.Model):
    label = models.CharField(max_length=80)
    endorsement = models.ForeignKey("Endorsement", on_delete=models.CASCADE, null=True)
