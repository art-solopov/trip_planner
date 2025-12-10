import datetime as dt
from collections import namedtuple

import pytest
from bs4 import BeautifulSoup

from trip_planner import db
from trip_planner.models import Point, PointTypes
from trip_planner.trips.presenters import PointPresenter
from test.factories import TripFactory, PointFactory


tp = namedtuple('tripandpoint', ['trip', 'point'])


@pytest.fixture
def trip(session_user):
    return TripFactory(author=session_user)


@pytest.fixture
def point(trip):
    return PointFactory(trip=trip)


def test_point_presenter_colors():
    assert PointPresenter.POINT_COLORS.keys() == set(PointTypes)


def test_point_edit_form(app_client, session_user, trip):
    point = PointFactory(trip=trip, type=PointTypes.ENTERTAINMENT.value)

    with app_client.session_transaction() as session:
        session['user_id'] = session_user.id
    res = app_client.get(f'/trips/{trip.key}/{point.id}/edit')
    assert res.status_code == 200

    soup = BeautifulSoup(res.data, 'html.parser')
    select = soup.find('select', attrs={'name': 'type'})
    option = select.find(lambda tag: tag['value'] == PointTypes.ENTERTAINMENT.value)
    assert 'selected' in option.attrs


def test_point_create_zero_latlon(app_client, session_user, trip):
    with app_client.session_transaction() as session:
        session['user_id'] = session_user.id

    data = {'name': 'Test point', 'lat': '0.00', 'lon': '0.00', 'type': 'museum'}
    res = app_client.post(f'/trips/{trip.key}/add-point', data=data)
    assert res.status_code in range(300, 400)

    assert Point.query.filter_by(trip=trip).count() == 1


class TestTripTouches:
    data = {'name': 'Point', 'type': 'museum', 'lat': '3.1415', 'lon': '1.2345'}

    @pytest.fixture(scope="function", autouse=True)
    def setup(self, app_client, session_user):
        with app_client.session_transaction() as session:
            session['user_id'] = session_user.id
        self.session_user = session_user
        self.app_client = app_client

    @pytest.fixture(scope='function', autouse=True)
    def __trip(self, session_user):
        created_at = dt.datetime.utcnow() - dt.timedelta(days=3)
        trip = TripFactory(author=session_user, created_at=created_at, updated_at=created_at)

        self.trip = trip

    def test_add_point(self):
        res = self.app_client.post(f'/trips/{self.trip.key}/add-point', data=self.data)
        assert res.status_code in range(300, 400)
        self._check_trip_touched()

    def test_edit_point(self):
        point = PointFactory(trip=self.trip, type=PointTypes.ENTERTAINMENT.value)
        res = self.app_client.post(f'/trips/{self.trip.key}/{point.id}/edit', data=self.data)
        assert res.status_code in range(300, 400)
        self._check_trip_touched()

    def test_delete_point(self):
        point = PointFactory(trip=self.trip, type=PointTypes.ENTERTAINMENT.value)
        res = self.app_client.post(f'/trips/{self.trip.key}/{point.id}/delete')
        assert res.status_code in range(300, 400)
        self._check_trip_touched()

    def _check_trip_touched(self):
        today = dt.datetime.combine(dt.datetime.utcnow().date(), dt.time())
        db.session.refresh(self.trip)
        assert self.trip.created_at < today
        assert self.trip.updated_at > today
