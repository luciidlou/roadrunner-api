from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from roadrunnerapi.models.freight_type import FreightType

# -------------------- SERIALIZERS --------------------


class FreightTypeSerializerGet(serializers.ModelSerializer):

    class Meta:
        model = FreightType
        fields = ('id', 'label', 'endorsement')
        depth = 1

# -----------------------------------------------------


class FreightTypeView(ViewSet):
    def list(self, request):
        """Retrives all of the freight types"""
        freight_types = FreightType.objects.all()
        serializer = FreightTypeSerializerGet(freight_types, many=True)
        return Response(serializer.data)
