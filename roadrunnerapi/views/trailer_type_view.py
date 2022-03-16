from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from roadrunnerapi.models import TrailerType


# -------------------- SERIALIZERS --------------------

class TrailerTypeSerializerGet(serializers.ModelSerializer):

    class Meta:
        model = TrailerType
        fields = ('id', 'label')
        depth = 1

# -----------------------------------------------------


class TrailerTypeView(ViewSet):
    def list(self, request):
        """Retrives all of the trailer types"""
        trailer_types = TrailerType.objects.all()
        serializer = TrailerTypeSerializerGet(trailer_types, many=True)
        return Response(serializer.data)
