from rest_framework import serializers
from messages_app.models import Message

class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = (
            'id',
            'contents',
            'recipient',
            'message_date',
        )