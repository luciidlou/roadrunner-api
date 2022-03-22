from django.contrib.auth.models import User
from django.db import models


class AppUser(models.Model):
    company = models.CharField(max_length=200)
    about = models.CharField(max_length=3500)
    established = models.DateField()
    user_type = models.CharField(max_length=15, blank=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
