from django.db import models


class Endorsement(models.Model):
    label = models.CharField(max_length=80)
