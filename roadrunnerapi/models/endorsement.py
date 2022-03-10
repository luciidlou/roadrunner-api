from django.db import models


class Endorsement(models.Model):
    letter = models.CharField(max_length=1)
    label = models.CharField(max_length=80)
