from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from song.models import Song
from song.serializers import SongSerializer
from django.core.exceptions import ValidationError
from song.helpers import validate_required_attributes, normalize_songs
from song.dbs import bulk_create_songs
import json

class SongPagination(PageNumberPagination):
    page_size = 10

class SongViewset(ModelViewSet):
    queryset = Song.objects.all().order_by('index')
    serializer_class = SongSerializer
    pagination_class = SongPagination
    filter_backends = [SearchFilter]
    search_fields = ['title']

    @action(detail=False, methods=['post'], url_path='upload-json')
    def upload_json(self, request):
        """View to accept JSON file and normalize data into the Song table."""
        json_file = request.FILES.get('file')
        if not json_file:
            return Response({"detail": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Load and validate JSON data
            data = json.load(json_file)
            validate_required_attributes(data)

            # Normalize and save data to the database
            normalized_songs = normalize_songs(data)
            bulk_create_songs(normalized_songs)

            return Response({"detail": "Songs data uploaded successfully"}, status=status.HTTP_201_CREATED)

        except json.JSONDecodeError:
            return Response({"detail": "Invalid JSON file"}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)