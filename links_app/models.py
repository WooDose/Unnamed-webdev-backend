from django.db import models

class Link(models.Model):
    name = models.CharField(max_length=255)
    uploader = models.ForeignKey(
        'posters_app.Poster',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    url = models.CharField(max_length=255)
    upload_date = models.DateField(auto_now_add=True)
    caption = models.CharField(max_length=255)
    likes = models.IntegerField()
    link_site = models.CharField(max_length=255, default='Unknown')

    def __str__(self):
        return 'Link {} uploaded by {} on {}. Link is: {}'.format(name, uploader, upload_date, url)

        