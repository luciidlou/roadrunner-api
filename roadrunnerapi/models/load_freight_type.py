from django.db import models


class LoadFreightType(models.Model):
    load = models.ForeignKey("Load", on_delete=models.CASCADE)
    freight_type = models.ForeignKey("FreightType", on_delete=models.CASCADE)
