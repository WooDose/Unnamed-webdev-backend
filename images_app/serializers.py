from rest_framework import serializers
from images_app.models import Image

class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = (
            'id',
            'name',
            'uploader',
            'directory',
            'upload_date',
            'caption',
            'likes',
            'dimensions',
        )