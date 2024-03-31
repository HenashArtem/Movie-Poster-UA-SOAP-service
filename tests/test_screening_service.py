import os
import shutil
import pytest
from app import app as flask_app
from services.screening_service import ScreeningService


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')
ORIGINAL_SCREENINGS_XML = os.path.join(DATA_DIR, 'screenings.xml')
COPY_SCREENINGS_XML = os.path.join(DATA_DIR, 'screenings_copy.xml')


@pytest.fixture(scope='function', autouse=True)
def setup_function():
    shutil.copyfile(ORIGINAL_SCREENINGS_XML, COPY_SCREENINGS_XML)

    yield
    shutil.copyfile(COPY_SCREENINGS_XML, ORIGINAL_SCREENINGS_XML)
    os.remove(COPY_SCREENINGS_XML)


@pytest.fixture(scope='function')
def client():
    return flask_app.test_client()


@pytest.fixture(scope='function')
def service():
    return ScreeningService()


def test_add_screening(client, service):
    movie_id = 1
    cinema_id = 1
    screening_id = 11
    time = "2024-04-10 20:00"
    response = service.add_screening(client, movie_id, cinema_id, screening_id, time)
    assert "added successfully" in response


def test_get_screening(client, service):
    screening_id = 1
    response = service.get_screening(client, screening_id)
    assert isinstance(response, dict)
    assert "not found" not in response.values()


def test_get_screenings(client, service):
    response = service.get_screenings(client)
    assert isinstance(response, list)
    assert len(response) > 0


def test_update_screening(client, service):
    screening_id = 1
    movie_id = 2
    cinema_id = 3
    time = "2024-04-10 21:00"
    response = service.update_screening(client, movie_id, cinema_id, screening_id, time)
    assert "updated successfully" in response.lower()


def test_delete_screening(client, service):
    screening_id = 1
    response = service.delete_screening(client, screening_id)
    assert "deleted successfully" in response.lower()


def test_delete_nonexistent_screening(client, service):
    screening_id = 1000
    response = service.delete_screening(client, screening_id)
    assert "not found" in response.lower()
