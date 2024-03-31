import os
import shutil
import pytest
from app import app as flask_app
from services.movie_service import MovieService


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')
ORIGINAL_MOVIES_XML = os.path.join(DATA_DIR, 'movies.xml')
COPY_MOVIES_XML = os.path.join(DATA_DIR, 'movies_copy.xml')


@pytest.fixture(scope='function', autouse=True)
def setup_function():
    shutil.copyfile(ORIGINAL_MOVIES_XML, COPY_MOVIES_XML)

    yield
    shutil.copyfile(COPY_MOVIES_XML, ORIGINAL_MOVIES_XML)
    os.remove(COPY_MOVIES_XML)


@pytest.fixture(scope='function')
def client():
    return flask_app.test_client()


@pytest.fixture(scope='function')
def service():
    return MovieService()


def test_add_movie(client, service):
    title = "Тестовий фільм"
    genre = "Страшна комедія"
    duration = "2 год"
    response = service.add_movie(client, title, genre, duration)
    assert "added successfully" in response


def test_get_movie(client, service):
    movie_id = 1
    response = service.get_movie(client, movie_id)
    assert isinstance(response, dict)
    assert "not found" not in response.values()


def test_get_movies(client, service):
    response = service.get_movies(client)
    assert isinstance(response, list)
    assert len(response) > 0


def test_update_movie(client, service):
    movie_id = 1
    title = "Оновлений фільм"
    genre = "Оновлена драма"
    duration = "1 год"
    response = service.update_movie(client, movie_id, title, genre, duration)
    assert "updated successfully" in response.lower()


def test_delete_movie(client, service):
    movie_id = 1
    response = service.delete_movie(client, movie_id)
    assert "deleted successfully" in response.lower()


def test_delete_nonexistent_movie(client, service):
    movie_id = 1000
    response = service.delete_movie(client, movie_id)
    assert "not found" in response.lower()
