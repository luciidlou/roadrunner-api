from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from roadrunnerapi.models import LoadHistory, Load, LoadStatus

# -------------------- SERIALIZERS --------------------


class LoadHistorySerializerGet(serializers.ModelSerializer):

    class Meta:
        model = LoadHistory
        fields = ('id', 'load', 'load_status', 'city', 'state', 'timestamp')
        depth = 1


class LoadHistorySerializerCreate(serializers.ModelSerializer):

    class Meta:
        model = LoadHistory
        fields = ('load', 'load_status', 'city', 'state')
        depth = 1

# -----------------------------------------------------


class LoadHistoryView(ViewSet):
    def retrieve(self, request, pk):
        """Retrives all of the LoadHistory objects for a load"""
        load = Load.objects.get(pk=pk)
        load_history = LoadHistory.objects.filter(load=load).order_by('-timestamp')
        serializer = LoadHistorySerializerGet(load_history, many=True)
        return Response(serializer.data)

    def create(self, request):
        """creates a LoadHistory object for a load"""
        load = Load.objects.get(pk=request.data['load'])

        if request.data['load_status'] is not None:
            load_status = LoadStatus.objects.get(
                pk=request.data['load_status'])
        else:
            load_status = None

        serializer = LoadHistorySerializerCreate(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(load=load, load_status=load_status)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
