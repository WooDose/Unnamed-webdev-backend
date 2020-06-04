from django.db import models

class Note(models.Model):
    title = models.CharField(max_length=30)
    uploader = models.ForeignKey(
        'posters_app.Poster',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    upload_date = models.DateField(auto_now_add=True)
    contents = models.CharField(max_length=5000)
    likes = models.IntegerField()

    def __str__(self):
        return 'Note {} uploaded by {} on {}. Content: {}'.format(title, uploader, upload_date, contents)

