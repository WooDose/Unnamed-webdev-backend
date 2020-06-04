from posters_app.models import Poster
from rest_framework import serializers

class PosterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Poster
        fields = (
            'id',
            'name',
            'display_picture',
            'date_joined',
        )