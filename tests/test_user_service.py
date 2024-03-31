import os
import shutil
import pytest
from app import app as flask_app
from services.user_service import UserService


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')
ORIGINAL_USERS_XML = os.path.join(DATA_DIR, 'users.xml')
COPY_USERS_XML = os.path.join(DATA_DIR, 'users_copy.xml')


@pytest.fixture(scope='function', autouse=True)
def setup_function():
    shutil.copyfile(ORIGINAL_USERS_XML, COPY_USERS_XML)

    yield
    shutil.copyfile(COPY_USERS_XML, ORIGINAL_USERS_XML)
    os.remove(COPY_USERS_XML)


@pytest.fixture(scope='function')
def client():
    return flask_app.test_client()


@pytest.fixture(scope='function')
def service():
    return UserService()


def test_add_user(client, service):
    username = "test_user"
    email = "test_user@example.com"
    response = service.add_user(client, username, email)
    assert "added successfully" in response


def test_get_user(client, service):
    user_id = 1
    response = service.get_user(client, user_id)
    assert isinstance(response, dict)
    assert "not found" not in response.values()


def test_get_users(client, service):
    response = service.get_users(client)
    assert isinstance(response, list)
    assert len(response) > 0


def test_update_user(client, service):
    user_id = 1
    username = "updated_user"
    email = "updated_user@example.com"
    response = service.update_user(client, user_id, username, email)
    assert "updated successfully" in response.lower()


def test_delete_user(client, service):
    user_id = 1
    response = service.delete_user(client, user_id)
    assert "deleted successfully" in response.lower()


def test_delete_nonexistent_user(client, service):
    user_id = 1000
    response = service.delete_user(client, user_id)
    assert "not found" in response.lower()
