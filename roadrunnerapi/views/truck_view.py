from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from roadrunnerapi.models import AppUser, Bid, Truck


# -------------------- SERIALIZERS --------------------

class TruckSerializerGet(serializers.ModelSerializer):

    class Meta:
        model = Truck
        fields = ('id', 'alias', 'trailer_type', 'dispatcher',
                  'current_city', 'current_state', 'is_assigned')
        depth = 1

# -----------------------------------------------------


class TruckView(ViewSet):
    def list(self, request):
        """Retrives all of the unbooked loads"""
        app_user = AppUser.objects.get(user=request.auth.user)
        if app_user.user_type == 'dispatcher':
            trucks = Truck.objects.filter(dispatcher=app_user)
            serializer = TruckSerializerGet(trucks, many=True)
            return Response(serializer.data)
        else:
            return Response(
                {'message': 'Distributors do not have access to the fleet manager'}
                )
