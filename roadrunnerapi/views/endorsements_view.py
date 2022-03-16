from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from roadrunnerapi.models import Endorsement


# -------------------- SERIALIZERS --------------------

class EndorsementSerializerGet(serializers.ModelSerializer):

    class Meta:
        model = Endorsement
        fields = ('id', 'letter' ,'label')
        depth = 1

# -----------------------------------------------------


class EndorsementView(ViewSet):
    def list(self, request):
        """Retrives all of the trailer types"""
        trailer_types = Endorsement.objects.all()
        serializer = EndorsementSerializerGet(trailer_types, many=True)
        return Response(serializer.data)
