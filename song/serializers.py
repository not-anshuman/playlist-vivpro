from rest_framework.serializers import ModelSerializer, SerializerMethodField, CharField
from song.models import Song
from django.db.models import Avg
from song.literals import SONG_FIELDS

class SongSerializer(ModelSerializer):
    average_rating = SerializerMethodField()
    vars()['class'] = SerializerMethodField()

    class Meta:
        model = Song
        fields = SONG_FIELDS

    def get_average_rating(self, obj):
        ratings = obj.ratings.all()
        if ratings:
            average = ratings.aggregate(Avg('rating'))['rating__avg']
            return round(average, 2)
        return 0
    
    def get_class(self, obj):
        return obj.song_class
    