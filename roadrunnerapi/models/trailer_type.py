from django.db import models


class TrailerType(models.Model):
    label = models.CharField(max_length=80)
