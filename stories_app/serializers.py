from rest_framework import serializers
from stories_app.models import Story

class StorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Story
        fields = (
            'id',
            'title',
            'uploader',
            'directory',
            'upload_date',
            'description',
            'image_count'
        )