from rest_framework import serializers
from soundbytes_app.models import Soundbyte

class SoundbyteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Soundbyte
        fields = (
            'id',
            'name',
            'uploader',
            'directory',
            'upload_date',
            'caption',
            'likes',
            'duration_sec',
        )
        