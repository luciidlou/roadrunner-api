from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from roadrunnerapi.models import Bid
from roadrunnerapi.models.app_user import AppUser

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
