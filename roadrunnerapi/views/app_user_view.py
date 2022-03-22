from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from roadrunnerapi.models import AppUser


# -------------------- SERIALIZERS --------------------

class AppUserSerializerGet(serializers.ModelSerializer):

    class Meta:
        model = AppUser
        fields = ('id', 'company', 'about', 'established', 'user')
        depth = 1

# -----------------------------------------------------


class AppUserView(ViewSet):
    def retrieve(self, request, pk):
        """Retrives a single app user"""
        app_user = AppUser.objects.get(pk=pk)
        serializer = AppUserSerializerGet(app_user)
        return Response(serializer.data)
