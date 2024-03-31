import os
import shutil
import pytest
from app import app as flask_app
from services.cinema_service import CinemaService


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')
ORIGINAL_CINEMAS_XML = os.path.join(DATA_DIR, 'cinemas.xml')
COPY_CINEMAS_XML = os.path.join(DATA_DIR, 'cinemas_copy.xml')


@pytest.fixture(scope='function', autouse=True)
def setup_function():
    shutil.copyfile(ORIGINAL_CINEMAS_XML, COPY_CINEMAS_XML)
    yield
    shutil.copyfile(COPY_CINEMAS_XML, ORIGINAL_CINEMAS_XML)
    os.remove(COPY_CINEMAS_XML)


@pytest.fixture(scope='function')
def client():
    return flask_app.test_client()


@pytest.fixture(scope='function')
def service():
    return CinemaService()


def test_add_cinema(client, service):
    name = "Тестовий кінотеатр"
    location = "Тестова адреса"
    movies_playing = "<movie_id>1</movie_id>"
    response = service.add_cinema(client, name, location, movies_playing)
    assert "added successfully" in response


def test_get_cinema(client, service):
    cinema_id = 1
    response = service.get_cinema(client, cinema_id)
    assert isinstance(response, dict)
    assert "not found" not in response.values()


def test_get_cinemas(client, service):
    response = service.get_cinemas(client)
    assert isinstance(response, list)
    assert len(response) > 0


def test_update_cinema(client, service):
    cinema_id = 1
    name = "Оновлений кінотеатр"
    location = "Оновлена адреса"
    movies_playing = "<movie_id>2</movie_id>"
    response = service.update_cinema(client, cinema_id, name, location, movies_playing)
    assert "updated successfully" in response.lower()


def test_delete_cinema(client, service):
    cinema_id = 1
    response = service.delete_cinema(client, cinema_id)
    assert "deleted successfully" in response.lower()


def test_delete_nonexistent_cinema(client, service):
    cinema_id = 1000
    response = service.delete_cinema(client, cinema_id)
    assert "not found" in response.lower()
