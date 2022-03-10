from django.db import models


class LoadStatus(models.Model):
    label = models.CharField(max_length=80)
