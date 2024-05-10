from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from song.models import Song
from rating.models import Rating
import json
import tempfile


class SongModelTest(TestCase):
    def setUp(self):
        self.song = Song.objects.create(
            index=1,
            id='5vYA1mW9g2Coh1HUFUSmlb',
            title='3AM',
            danceability=0.521,
            energy=0.673,
            key=8,
            loudness=-8.685,
            mode=1,
            acousticness=0.00573,
            instrumentalness=0.0,
            liveness=0.12,
            valence=0.543,
            tempo=108.031,
            duration_ms=225947,
            time_signature=4,
            num_bars=100,
            num_sections=8,
            num_segments=830,
            song_class=1
        )

    def test_song_creation(self):
        """Test that a song instance is created successfully."""
        self.assertEqual(str(self.song), '3AM')

    def test_song_fields(self):
        """Test that all fields are correctly set."""
        self.assertEqual(self.song.index, 1)
        self.assertEqual(self.song.id, '5vYA1mW9g2Coh1HUFUSmlb')
        self.assertEqual(self.song.title, '3AM')
        self.assertEqual(self.song.danceability, 0.521)
        self.assertEqual(self.song.energy, 0.673)
        self.assertEqual(self.song.key, 8)
        self.assertEqual(self.song.loudness, -8.685)
        self.assertEqual(self.song.mode, 1)

class SongViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.song = Song.objects.create(
            index=1,
            id='5vYA1mW9g2Coh1HUFUSmlb',
            title='3AM',
            danceability=0.521,
            energy=0.673,
            key=8,
            loudness=-8.685,
            mode=1,
            acousticness=0.00573,
            instrumentalness=0.0,
            liveness=0.12,
            valence=0.543,
            tempo=108.031,
            duration_ms=225947,
            time_signature=4,
            num_bars=100,
            num_sections=8,
            num_segments=830,
            song_class=1
        )
        Rating.objects.create(song=self.song, rating=4)
        Rating.objects.create(song=self.song, rating=5)

    def test_list_songs(self):
        """Test listing songs via the API."""
        response = self.client.get('/songs/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['results']), 1)
        self.assertEqual(response.json()['results'][0]['title'], '3AM')
        self.assertEqual(response.json()['results'][0]['average_rating'], 4.5)
        print(response.json()['results'][0])

    def test_retrieve_song(self):
        """Test retrieving a single song via the API."""
        response = self.client.get(f'/songs/{self.song.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['title'], '3AM')
        self.assertEqual(response.json()['average_rating'], 4.5)

    def test_search_songs(self):
        """Test searching songs via the API."""
        Song.objects.create(
            index=2,
            id='5vYA1mW9g2Coh1HUFUSmlc',
            title='4AM',
            danceability=0.521,
            energy=0.673,
            key=8,
            loudness=-8.685,
            mode=1,
            acousticness=0.00573,
            instrumentalness=0.0,
            liveness=0.12,
            valence=0.543,
            tempo=108.031,
            duration_ms=225947,
            time_signature=4,
            num_bars=100,
            num_sections=8,
            num_segments=830,
            song_class=1
        )
        response = self.client.get('/songs/?search=3AM')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['results']), 1)
        self.assertEqual(response.json()['results'][0]['title'], '3AM')

    def test_upload_json(self):
        """Test uploading a JSON file via the API."""
        json_content = {
            "index": {"0": 2},
            "id": {"0": "5vYA1mW9g2Coh1HUFUSmlc"},
            "title": {"0": "4AM"},
            "danceability": {"0": 0.521},
            "energy": {"0": 0.673},
            "key": {"0": 8},
            "loudness": {"0": -8.685},
            "mode": {"0": 1},
            "acousticness": {"0": 0.00573},
            "instrumentalness": {"0": 0.0},
            "liveness": {"0": 0.12},
            "valence": {"0": 0.543},
            "tempo": {"0": 108.031},
            "duration_ms": {"0": 225947},
            "time_signature": {"0": 4},
            "num_bars": {"0": 100},
            "num_sections": {"0": 8},
            "num_segments": {"0": 830},
            "class": {"0": 1}
        }

        with tempfile.NamedTemporaryFile(mode='w+', suffix='.json') as temp_file:
            json.dump(json_content, temp_file)
            temp_file.seek(0)
            response = self.client.post('/songs/upload-json/', {'file': temp_file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Song.objects.count(), 2)