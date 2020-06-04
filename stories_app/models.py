from django.db import models

class Story(models.Model):
    title = models.CharField(max_length=255)
    uploader = models.ForeignKey(
        'posters_app.Poster',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    directory = models.CharField(max_length=255)
    upload_date = models.DateField(auto_now_add=True)
    description = models.CharField(max_length=255)
    image_count = models.IntegerField(default=1)
    def __str__(self):
        return 'Story {} uploaded by {} on {}. Contents on directory {}'.format(name, uploader, upload_date, directory)

