from django.db import models

class Notification(models.Model):
    notification_type = models.CharField(max_length=12)
    recipient = models.ForeignKey(
        'posters_app.Poster',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    notification_date = models.DateField(auto_now_add=True)


    def __str__(self):
        return 'Notification of type: {} sent to user {} on date {}'.format(notification_type,recipient,notification_date)

