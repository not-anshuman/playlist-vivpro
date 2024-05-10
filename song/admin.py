from django.contrib import admin
from song.models import Song

class SongAdmin(admin.ModelAdmin):
    list_display = ('index', 'id', 'title', 'danceability', 'energy', 'key', 'loudness',
                    'mode', 'acousticness', 'instrumentalness', 'liveness', 'valence',
                    'tempo', 'duration_ms', 'time_signature', 'num_bars', 'num_sections',
                    'num_segments', 'song_class')
    search_fields = ('title', 'id')
    list_filter = ('key', 'mode', 'time_signature')
    ordering = ('index',)

admin.site.register(Song, SongAdmin)
