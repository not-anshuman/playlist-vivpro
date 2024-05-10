from django.db import models
from song.models import Song

class Rating(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='ratings')
    rating = models.IntegerField()
