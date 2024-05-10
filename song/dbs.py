from django.db import transaction
from song.models import Song

def bulk_create_songs(songs):
    """Insert a list of Song instances into the database using bulk_create."""
    with transaction.atomic():
        Song.objects.bulk_create(songs, ignore_conflicts=True)
