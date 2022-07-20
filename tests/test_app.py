from datetime import datetime
from unittest.mock import patch
import pytest
import db
import app


@pytest.fixture
def testing_client():
    with app.app.test_client() as client:
        yield client


@pytest.fixture
def testing_session():
    with patch("db.get_session"):
        yield


@pytest.fixture
def testing_tasks():
    task_1 = db.Task(id=1, title='Do homework', description='Do math', date=datetime(2020, 12, 12), is_done=False)
    task_2 = db.Task(id=2, title='Wishlist', description='Milk', date=datetime(2021, 2, 18), is_done=False)
    task_3 = db.Task(id=3, title='Make a cake', description='First, second', date=datetime(2021, 8, 22), is_done=True)
    yield [task_1, task_2, task_3]


def test_get_tasks(testing_client, testing_session, testing_tasks):
    with patch("db.get_all_tasks", return_value=testing_tasks) as mock:
        response = testing_client.get(app.ROOT_URL)
        assert response.status_code == 200
        assert response.json == [task.as_dict() for task in testing_tasks]
        mock.assert_called_once()


def test_get_task(testing_client, testing_session, testing_tasks):
    task = testing_tasks[0]
    with patch("db.get_task", return_value=task) as mock:
        response = testing_client.get(f"{app.ROOT_URL}/1")
        assert response.status_code == 200
        assert response.json == task.as_dict()
        assert mock.call_args.args[1] == 1


@pytest.mark.parametrize('task_id', ('1a', 'a2b', 'ab', 'ab3'))
def test_get_task_invalid_task_id(testing_client, testing_session, task_id):
    with patch("db.get_task"):
        response = testing_client.get(f'{app.ROOT_URL}/{task_id}')
        assert response.status_code == 400
        assert response.json["message"] == "Invalid task_id"


@pytest.mark.parametrize('task_id', ('111', '222', '333', '444'))
def test_get_task_no_task(testing_client, testing_session, task_id):
    with patch("db.get_task", return_value=False):
        response = testing_client.get(f'{app.ROOT_URL}/{task_id}')
        assert response.status_code == 404
        assert response.json["message"] == "No such task"


def test_create_task_no(testing_client, testing_session):
    with patch("db.add_task", return_value=1):
        response = testing_client.post(app.ROOT_URL, json={"title": "Buy milk", "date": "2022-7-12", "description": "go to shop take money"})
        assert response.status_code == 201
        assert response.json["message"] == "Task id=1 has been created"


def test_create_task_without_json(testing_client, testing_session):
    with patch("db.add_task", return_value=1):
        response = testing_client.post(app.ROOT_URL)
        assert response.status_code == 400


def test_delete_task(testing_client, testing_session):
    with patch("db.delete_task", return_value=True) as mock:
        response = testing_client.delete(f'{app.ROOT_URL}/1')
        assert response.status_code == 200
        assert response.json["message"] == "Task id=1 has been deleted"
        mock.assert_called_once()


def test_delete_task_no_task(testing_client, testing_session):
    with patch("db.delete_task", return_value=False) as mock:
        response = testing_client.delete(f'{app.ROOT_URL}/1')
        assert response.status_code == 404
        assert response.json["message"] == "No such task"
        mock.assert_called_once()


def test_update_task(testing_client, testing_session):
    with patch("db.change_task_status", return_value=True) as mock:
        response = testing_client.put(f'{app.ROOT_URL}/1/status')
        assert response.status_code == 200
        assert response.json["message"] == "Task id=1 marked as ready"
        mock.assert_called_once()


def test_update_task_no_task(testing_client, testing_session):
    with patch("db.change_task_status", return_value=False) as mock:
        response = testing_client.put(f'{app.ROOT_URL}/1/status')
        assert response.status_code == 404
        assert response.json["message"] == "No such task"
        mock.assert_called_once()
