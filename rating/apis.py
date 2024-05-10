from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from song.models import Song
from rating.models import Rating

@api_view(['POST'])
def rate_song(request, song_id):
    try:
        song = Song.objects.get(pk=song_id)
    except Song.DoesNotExist:
        return Response({'message': 'Song not found'}, status=status.HTTP_404_NOT_FOUND)
    
    rating_value = request.data.get('rating')
    
    if not rating_value or not (1 <= int(rating_value) <= 5):
        return Response({'message': 'Rating must be an integer between 1 and 5'}, status=status.HTTP_400_BAD_REQUEST)
    
    Rating.objects.create(
        song=song, rating=rating_value
    )
    
    return Response({'message': 'Rating added', 'rating': rating_value})
