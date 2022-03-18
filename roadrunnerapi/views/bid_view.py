from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from roadrunnerapi.models import AppUser, Bid, Load
from roadrunnerapi.models.load_status import LoadStatus
from roadrunnerapi.models.truck import Truck

# -------------------- SERIALIZERS --------------------


class BidSerializerGet(serializers.ModelSerializer):

    class Meta:
        model = Bid
        fields = ('id', 'load', 'truck', 'dispatcher',
                  'dollar_amount', 'is_accepted', 'is_owner',
                  'timestamp')
        depth = 2

# -----------------------------------------------------


class BidView(ViewSet):
    def list(self, request):
        """Retrives all of the Bid objects"""
        app_user = AppUser.objects.get(user=request.auth.user)
        bids = Bid.objects.all()
        for bid in bids:
            if bid.dispatcher == app_user:
                bid.is_owner = True
            else:
                bid.is_owner = False
        serializer = BidSerializerGet(bids, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        """Retrieves a single Bid object"""
        app_user = AppUser.objects.get(user=request.auth.user)
        bid = Bid.objects.get(pk=pk)

        if bid.dispatcher == app_user:
            bid.is_owner = True
        else:
            bid.is_owner = False

        serializer = BidSerializerGet(bid)
        return Response(serializer.data)

    def destroy(self, request, pk):
        """Deletes a single Bid object"""
        bid = Bid.objects.get(pk=pk)
        bid.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=True)
    def loadbids(self, request, pk):
        """Retrives all of the Bid objects that belong to a particular load"""
        app_user = AppUser.objects.get(user=request.auth.user)
        bids = Bid.objects.filter(load_id=pk)

        for bid in bids:
            if bid.dispatcher == app_user:
                bid.is_owner = True
            else:
                bid.is_owner = False

        serializer = BidSerializerGet(bids, many=True)
        return Response(serializer.data)

    @action(methods=['put'], detail=True)
    def accept(self, request, pk):
        """Retrives all of the Bid objects that belong to a particular load"""
        bid = Bid.objects.get(pk=pk)
        load = Load.objects.get(pk=request.data['load']['id'])
        truck = Truck.objects.get(pk=request.data['truck']['id'])
        initial_status = LoadStatus.objects.get(pk=1)

        if load.is_booked is False:
            bid.is_accepted = True
            bid.save()

            load.is_booked = True
            load.load_status = initial_status
            load.save()

            truck.is_assigned = True
            truck.save()
        else:
            bid.is_accepted = False
            bid.save()

            load.is_booked = False
            load.load_status = None
            load.save()

            truck.is_assigned = False
            truck.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
