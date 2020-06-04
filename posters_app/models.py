from django.db import models
##Posters are users.


class Poster(models.Model):
    name = models.CharField(max_length=15)
    display_picture = models.CharField(max_length=255)
    date_joined = models.DateField(auto_now_add=True)

    def __str__(self):
        return "User with nickname {}, joined on {}".format(self.name, self.date_joined)
