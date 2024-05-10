from django.test import TestCase
from song.models import Song
from rating.models import Rating
from rest_framework import status
from rest_framework.test import APIClient, APITestCase


class RatingModelTest(TestCase):
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

    def test_rating_creation(self):
        """Test that a rating instance is created successfully."""
        rating = Rating.objects.create(song=self.song, rating=4)
        self.assertEqual(rating.rating, 4)
        self.assertEqual(str(rating.song), '3AM')


class RateSongApiTest(APITestCase):
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

    def test_rate_song(self):
        """Test that a user can rate a song successfully."""
        response = self.client.post(
            f'/rate-song/{self.song.id}/',
            {'rating': 4},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Rating.objects.count(), 1)
        rating = Rating.objects.get(song=self.song)
        self.assertEqual(rating.rating, 4)
        self.assertEqual(response.json()['message'], 'Rating added')

    def test_rate_song_invalid_value(self):
        """Test that rating with an invalid value returns a 400 status."""
        response = self.client.post(
            f'/rate-song/{self.song.id}/',
            {'rating': 6},  # Invalid rating value
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['message'], 'Rating must be an integer between 1 and 5')

    def test_rate_nonexistent_song(self):
        """Test that rating a nonexistent song returns a 404 status."""
        response = self.client.post(
            '/rate-song/nonexistent_id/',
            {'rating': 4},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json()['message'], 'Song not found')
