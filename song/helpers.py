from django.core.exceptions import ValidationError
from song.literals import JSON_IMPORT_REQUIRED_ATTRIBUTES
from song.models import Song

def validate_required_attributes(data):
    """Validate that the required attributes are present in the JSON data."""
    missing_attributes = JSON_IMPORT_REQUIRED_ATTRIBUTES - set(data.keys())
    if missing_attributes:
        raise ValidationError(f"Missing required attributes: {', '.join(missing_attributes)}")

def normalize_songs(data):
    """Normalize the JSON data into a list of Song instances."""
    normalized_songs = []
    # Infer indices dynamically from any key present in the JSON file
    first_key = list(data.keys())[0]
    indices = data[first_key].keys()

    for idx in indices:
        song_attributes = {attr: data[attr][idx] for attr in JSON_IMPORT_REQUIRED_ATTRIBUTES}
        song_attributes['index'] = int(idx)
        # Map the `class` attribute to `song_class`
        song_attributes['song_class'] = song_attributes.pop('class')
        normalized_songs.append(Song(**song_attributes))

    return normalized_songs
