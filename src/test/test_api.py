import random
import pytest
from fastapi.testclient import TestClient
from auth.user import User
from main import app
from reservation.domain.table import Table
from unit_of_work import UnitOfWork, get_test_uow, get_uow
from project_orm import TEST_SESSION_FACTORY
from backbone.base_class import Base
from project_orm import TEST_BIND
from project_config import SEAT_PRICE, TABLE_COUNT, SEAT_COUNT

username = "string"
password = "string"
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzdHJpbmcifQ.BaxNx__C7XsKtycVU0Cw05wv_rh-EF8KyOl7wwlTnmY"

random_odd = lambda: random.randrange(1, SEAT_COUNT, 2)
random_even = lambda: random.randrange(2, SEAT_COUNT, 2)


@pytest.fixture(scope="function")
def test_client():
    from reservation import domain as reservation_domain

    Base.metadata.drop_all(bind=TEST_BIND)
    Base.metadata.create_all(bind=TEST_BIND)

    with UnitOfWork(session_factory=TEST_SESSION_FACTORY) as uow:
        for i in range(TABLE_COUNT):
            table = Table(table_number=f"table{i}", available_seats=SEAT_COUNT)
            uow.session.add(table)
        user = User(username=username, password=username)
        uow.session.add(user)
        uow.commit()

    app.dependency_overrides[get_uow] = get_test_uow

    client = TestClient(app)
    yield client

    Base.metadata.drop_all(bind=TEST_BIND)


def test_book_without_token(test_client):
    response = test_client.post(
        "/book",
        json={
            "people_count": SEAT_COUNT,
        },
    )
    assert response.status_code == 401, response.text


def test_cancel_without_token(test_client):
    response = test_client.delete(
        "/cancel/1",
    )
    assert response.status_code == 401, response.text


def test_number_of_people_equal_to_seat_count(test_client):
    response = test_client.post(
        "/book",
        json={
            "people_count": SEAT_COUNT,
        },
        headers={"Authorization": token},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["seat_count"] == SEAT_COUNT
    assert data["total_price"] == (SEAT_COUNT - 1) * SEAT_PRICE


def test_odd_number_of_people_not_equal_to_seat_count(test_client):
    people_count = random_odd()
    response = test_client.post(
        "/book",
        json={
            "people_count": people_count,
        },
        headers={"Authorization": token},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["seat_count"] == people_count + 1
    assert data["total_price"] == (people_count + 1) * SEAT_PRICE


def test_even_number_of_people_not_equal_to_seat_count(test_client):
    people_count = random_even()
    response = test_client.post(
        "/book",
        json={
            "people_count": people_count,
        },
        headers={"Authorization": token},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["seat_count"] == people_count
    assert data["total_price"] == people_count * SEAT_PRICE


def test_cancel_reservation(test_client):
    create_response = test_client.post(
        "/book",
        json={
            "people_count": SEAT_COUNT,
        },
        headers={"Authorization": token},
    )
    data = create_response.json()
    reservation_id = data["id"]

    delete_response = test_client.delete(
        f"/cancel/{reservation_id}",
        headers={"Authorization": token},
    )
    assert delete_response.status_code == 200, delete_response.text
