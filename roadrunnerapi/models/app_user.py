from django.contrib.auth.models import User
from django.db import models


class AppUser(models.Model):
    company = models.CharField(max_length=200)
    about = models.CharField(max_length=3500)
    established = models.DateField()
    user_type = models.CharField(max_length=15, blank=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    @property
    def avg_rating(self):  # pylint: disable=missing-function-docstring
        return self.__avg_rating

    @avg_rating.setter
    def avg_rating(self, value):
        self.__avg_rating = value
