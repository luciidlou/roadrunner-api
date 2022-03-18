from django.db import models

# from roadrunnerapi.models import Load, Bid


class Truck(models.Model):
    """Model for a Truck object"""
    alias = models.CharField(max_length=120)
    trailer_type = models.ForeignKey("TrailerType", on_delete=models.CASCADE)
    dispatcher = models.ForeignKey("AppUser", on_delete=models.CASCADE)
    current_city = models.CharField(max_length=300)
    current_state = models.CharField(max_length=2)
    is_assigned = models.BooleanField(default=False)
    endorsements = models.ManyToManyField(
        "Endorsement", through="TruckEndorsement", related_name="endorsements")
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    retired_on = models.DateTimeField(null=True)

    @property
    def current_load(self):
        """if truck is currently assigned a load, returns that load"""
        return self.__current_load

    @current_load.setter
    def current_load(self, value):
        self.__current_load = value


# ? WHY CAN'T I DO THIS. WTF IS A CIRCULAR IMPORT??? (SEE IMPORTS ON LINE 3)

    # @property
    # def load_count(self):
    #     loads_list = []
    #     bids = Bid.objects.filter(is_accepted=True, truck=self)
    #     loads = Load.objects.filter(is_booked=True)
    #     for bid in bids:
    #         for load in loads:
    #             if bid.load == load:
    #                 loads_list.append(load)

    #     return len(loads_list)
