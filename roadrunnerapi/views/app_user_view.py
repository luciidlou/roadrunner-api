from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from roadrunnerapi.models import AppUser, DispatcherRating


# -------------------- SERIALIZERS --------------------

class AppUserSerializerGet(serializers.ModelSerializer):

    class Meta:
        model = AppUser
        fields = ('id', 'company', 'about', 'established',
                  'user', 'user_type', 'avg_rating')
        depth = 1

# -----------------------------------------------------


class AppUserView(ViewSet):
    def retrieve(self, request, pk):
        """Retrives a single app user"""
        app_user = AppUser.objects.get(pk=pk)

        if app_user.user_type == 'dispatcher':
            ratings = DispatcherRating.objects.filter(dispatcher=app_user)
            if len(ratings) != 0:
                total_rating = 0
                for rating in ratings:
                    total_rating += rating.rating
                app_user.avg_rating = total_rating / len(ratings)
            else:
                app_user.avg_rating = 0

        serializer = AppUserSerializerGet(app_user)
        return Response(serializer.data)
