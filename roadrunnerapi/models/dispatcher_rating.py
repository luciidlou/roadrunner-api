from django.db import models


class DispatcherRating(models.Model):
    distributor = models.ForeignKey("AppUser", on_delete=models.CASCADE, related_name="distributor")
    dispatcher = models.ForeignKey("AppUser", on_delete=models.CASCADE, related_name="dispatcher")
    rating = models.FloatField()


    @property
    def is_rater(self):  # pylint: disable=missing-function-docstring
        return self.__is_rater

    @is_rater.setter
    def is_rater(self, value):
        self.__is_rater = value
