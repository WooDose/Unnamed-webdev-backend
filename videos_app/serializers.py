from rest_framework import serializers
from videos_app.models import Video

class VideoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Video
        fields = (
            'id',
            'name',
            'uploader',
            'directory',
            'upload_date',
            'caption',
            'likes',
            'dimensions',
            'duration_secs',
        )