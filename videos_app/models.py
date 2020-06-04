from django.db import models

class Video(models.Model):
    name = models.CharField(max_length=255)
    uploader = models.ForeignKey(
        'posters_app.Poster',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    directory = models.CharField(max_length=255)
    upload_date = models.DateField(auto_now_add=True)
    caption = models.CharField(max_length=255)
    likes = models.IntegerField()
    dimensions = models.CharField(max_length=255, default='600x800')
    duration_secs = models.IntegerField(default='6')

    def __str__(self):
        return 'Video {} uploaded by {} on {}. Can be found on directory {}'.format(name, uploader, upload_date, directory)

