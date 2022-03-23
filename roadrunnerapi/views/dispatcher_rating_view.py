from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from roadrunnerapi.models import AppUser, DispatcherRating

# -------------------- SERIALIZERS --------------------


class RatingSerializerGet(serializers.ModelSerializer):

    class Meta:
        model = DispatcherRating
        fields = ('id', 'distributor', 'dispatcher', 'rating', 'is_rater')
        depth = 1


class RatingSerializerCreate(serializers.ModelSerializer):

    class Meta:
        model = DispatcherRating
        fields = ('dispatcher', 'rating')

# -----------------------------------------------------


class DispatcherRatingView(ViewSet):
    def retrieve(self, request, pk):
        """Retrieves a single the DispatcherRating object"""
        distributor = AppUser.objects.get(user=request.auth.user)
        dispatcher = AppUser.objects.get(pk=pk)

        try:
            rating = DispatcherRating.objects.get(
                distributor=distributor, dispatcher=dispatcher)
            rating.is_rater = distributor == rating.distributor
        except DispatcherRating.DoesNotExist:
            return Response("")

        serializer = RatingSerializerGet(rating)
        return Response(serializer.data)

    def create(self, request):
        """Creates a DispatcherRating object"""
        distributor = AppUser.objects.get(user=request.auth.user)
        dispatcher = AppUser.objects.get(pk=request.data['dispatcher'])
        serializer = RatingSerializerCreate(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save(distributor=distributor, dispatcher=dispatcher)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Updates a DispatcherRating object"""
        rating = DispatcherRating.objects.get(pk=pk)

        rating.rating = request.data['rating']

        rating.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """Deletes a DispatcherRating object"""
        rating = DispatcherRating.objects.get(pk=pk)

        rating.delete()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
