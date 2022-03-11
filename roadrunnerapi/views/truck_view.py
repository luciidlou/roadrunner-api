from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from roadrunnerapi.models import AppUser, Truck, Bid
from roadrunnerapi.serializers import LoadSerializerGet


class TruckView(ViewSet):
    def list(self, request):
        """Retrives all of the unbooked loads"""
        app_user = AppUser.objects.get(user=request.auth.user)
        trucks = Truck.objects.filter(dispatcher=app_user)
        serializer = LoadSerializerGet(trucks, many=True)
        return Response(serializer.data)
