from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from song.apis import SongViewset
from rating.apis import rate_song

router = DefaultRouter()
router.register(r'songs', SongViewset)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('rate-song/<str:song_id>/', rate_song, name='rate_song'),
]
