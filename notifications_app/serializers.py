from rest_framework import serializers
from notifications_app.models import Notification

class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = (
            'id',
            'notification_type',
            'recipient',
            'notification_date'
        )