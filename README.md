Music Playlist API Project

This is a Django-based API project that allows users to upload and view song playlists. The API provides endpoints for listing songs, searching by title, retrieving specific songs, and rating songs. Additionally, a Postman Collection has been included for testing the API endpoints.
Prerequisites

Before you begin, ensure you have the following installed:

Python: 3.12.3
Poetry: 1.8.2

Poetry can be installed by:
```
pip install poetry==1.8.2
```

----------------------------------------------------------------------------------------------

Getting Started

Follow these steps to set up the project locally.
1. Clone the Repository

```
git clone [<repository-url>](https://github.com/not-anshuman/playlist-vivpro.git)
cd playlist-vivpro
```

2. Install Dependencies

```
poetry install
```

3. Apply Migrations

```
poetry run python manage.py migrate
```

4. Run the Development Server

```
poetry run python manage.py runserver
```

----------------------------------------------------------------------------------------------

API Usage
Endpoints

Here's a quick overview of the API endpoints.

- Upload JSON Data

  Endpoint: POST /songs/upload-json/
  Description: Upload a playlist JSON file and normalize it into the Song table.
  Example Request:
  ```
  curl -X POST http://localhost:8000/songs/upload-json/ \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/playlist.json"
  ```

- List All Songs

  Endpoint: GET /songs/?page=<number>
  Description: List all songs with pagination.
  Example Request:
  ```
  curl -X GET http://localhost:8000/songs/?page=1
  ```

- Search Song by Title

  Endpoint: GET /songs/?search=<title>
  Description: Search songs by title.
  Example Request:
  ```
  curl -X GET http://localhost:8000/songs/?search=3AM
  ```

- Retrieve a Specific Song

  Endpoint: GET /songs/{id}/
  Description: Retrieve a specific song by ID.
  Example Request:
  ```
  curl -X GET http://localhost:8000/songs/5vYA1mW9g2Coh1HUFUSmlb/
  ```

- Rate a Song

  Endpoint: POST /rate-song/{id}/
  Description: Rate a song (1-5 stars).
  Example Request:
  ```
  curl -X POST http://localhost:8000/rate-song/5vYA1mW9g2Coh1HUFUSmlb/ \
  -H "Content-Type: application/json" \
  -d '{
    "rating": 5
  }'
  ```

----------------------------------------------------------------------------------------------

Postman Collection

To simplify testing, a Postman Collection is included:

  Import the Collection:
      Open Postman.
      Click Import.
      Select the JSON file: Music Playlist API.postman_collection.json.
  Use the Predefined Requests to interact with the API.
