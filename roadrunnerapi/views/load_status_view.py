from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from roadrunnerapi.models.load_status import LoadStatus

# -------------------- SERIALIZERS --------------------


class LoadStatusSerializerGet(serializers.ModelSerializer):

    class Meta:
        model = LoadStatus
        fields = ('id', 'label')
        depth = 1

# -----------------------------------------------------


class LoadStatusView(ViewSet):
    def list(self, request):
        """Retrives all of the freight types"""
        load_status_all = LoadStatus.objects.all()
        serializer = LoadStatusSerializerGet(load_status_all, many=True)
        return Response(serializer.data)
