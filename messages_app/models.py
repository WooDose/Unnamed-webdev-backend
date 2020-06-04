from django.db import models

class Message(models.Model):
    contents = models.CharField(max_length=255, null=False, blank=False)
    recipient = models.ForeignKey(
        'posters_app.Poster',
        on_delete=models.SET_NULL,
        null=True
    )
    message_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return 'Anonymous message sent to {}: {}'.format(recipient, contents)


