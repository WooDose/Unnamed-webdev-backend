from rest_framework import serializers
from notes_app.models import Note

class NoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Note
        fields = (
            'id',
            'title',
            'uploader',
            'upload_date',
            'contents',
            'likes',
        )