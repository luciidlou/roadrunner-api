from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from roadrunnerapi.models import Bid, Load

# -------------------- SERIALIZERS --------------------


class BidSerializerGet(serializers.ModelSerializer):

    class Meta:
        model = Bid
        fields = ('id', 'label', 'endorsement')
        depth = 1

# -----------------------------------------------------


class BidView(ViewSet):
    def list(self, request):
        """Retrives all of the freight types"""
        freight_types = Bid.objects.all()
        serializer = BidSerializerGet(freight_types, many=True)
        return Response(serializer.data)
