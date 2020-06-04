from rest_framework import serializers
from links_app.models import Link

class LinkSerializer(serializers.ModelSerializer):

    class Meta:
        model = Link
        fields = (
            'id',
            'name',
            'uploader',
            'url',
            'upload_date',
            'caption',
            'likes',
            'link_site',
        )