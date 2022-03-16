from django.db import models


class Bid(models.Model):
    load = models.ForeignKey("Load", on_delete=models.CASCADE)
    truck = models.ForeignKey("Truck", on_delete=models.CASCADE)
    dispatcher = models.ForeignKey("AppUser", on_delete=models.CASCADE)
    dollar_amount = models.FloatField()
    is_accepted = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    @property
    def is_owner(self):
        """Checks to see if the load is owned by the current user. Returns boolean"""
        return self.__is_owner

    @is_owner.setter
    def is_owner(self, value):
        self.__is_owner = value
