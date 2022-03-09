from django.db import models
from django.contrib.auth.models import User

class TrailerType(models.Model):
    label = models.CharField(max_length=80)