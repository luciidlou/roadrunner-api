from rest_framework import serializers
from roadrunnerapi.models import Load


class LoadSerializerGet(serializers.ModelSerializer):

    class Meta:
        model = Load
        fields = ('id', 'distributor', 'created_on', 'pickup_address', 'pickup_city',
                  'pickup_state', 'pickup_datetime', 'dropoff_address', 'dropoff_city',
                  'dropoff_state', 'dropoff_datetime', 'distance', 'is_hazardous',
                  'is_booked', 'load_status')
        depth = 2
