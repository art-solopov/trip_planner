import datetime as dt

from bs4 import BeautifulSoup

from trip_planner.models import Trip, Point, PointTypes
from trip_planner.trips.presenters import PointPresenter
from test.factories import TripFactory, PointFactory


def test_point_presenter_colors():
    assert PointPresenter.POINT_COLORS.keys() == set(PointTypes)


def test_point_edit_form(app_client, db_session, session_user):
    trip = TripFactory(author=session_user)
    point = PointFactory(trip=trip, type=PointTypes.ENTERTAINMENT.value)
    db_session.add(trip)
    db_session.add(point)
    db_session.commit()

    with app_client.session_transaction() as session:
        session['user_id'] = session_user.id
    res = app_client.get(f'/trips/{trip.key}/{point.id}/edit')
    assert res.status_code == 200

    soup = BeautifulSoup(res.data, 'html.parser')
    select = soup.find('select', attrs={'name': 'type'})
    option = select.find(lambda tag: tag['value'] == PointTypes.ENTERTAINMENT.value)
    assert 'selected' in option.attrs


def test_point_create_zero_latlon(app_client, db_session, session_user):
    trip = TripFactory(author=session_user)
    db_session.add(trip)
    db_session.commit()

    with app_client.session_transaction() as session:
        session['user_id'] = session_user.id

    data = {'name': 'Test point', 'lat': '0.00', 'lon': '0.00', 'type': 'museum'}
    res = app_client.post(f'/trips/{trip.key}/add-point', data=data)
    assert res.status_code in range(300, 400)

    assert Point.query.filter_by(trip=trip).count() == 1


def test_add_point_touches_trip(app_client, db_session, session_user):
    created_at = dt.datetime.utcnow() - dt.timedelta(days=3)
    today = dt.datetime.combine(dt.date.today(), dt.time())
    trip = TripFactory(author=session_user, created_at=created_at, updated_at=created_at)
    db_session.add(trip)
    db_session.commit()

    with app_client.session_transaction() as session:
        session['user_id'] = session_user.id

    data = {'name': 'Point', 'type': 'museum', 'lat': '3.1415', 'lon': '1.2345'}
    res = app_client.post(f'/trips/{trip.key}/add-point', data=data)
    assert res.status_code in range(300, 400)

    db_session.refresh(trip)
    assert trip.created_at < today
    assert trip.updated_at > today


def test_edit_point_touches_trip(app_client, db_session, session_user):
    created_at = dt.datetime.utcnow() - dt.timedelta(days=3)
    today = dt.datetime.combine(dt.date.today(), dt.time())

    trip = TripFactory(author=session_user, created_at=created_at, updated_at=created_at)
    point = PointFactory(trip=trip, type=PointTypes.ENTERTAINMENT.value)
    db_session.add(trip)
    db_session.add(point)
    db_session.commit()

    with app_client.session_transaction() as session:
        session['user_id'] = session_user.id

    data = {'name': 'Point', 'type': 'museum', 'lat': '3.1415', 'lon': '1.2345'}
    res = app_client.post(f'/trips/{trip.key}/{point.id}/edit', data=data)
    assert res.status_code in range(300, 400)

    db_session.refresh(trip)
    assert trip.created_at < today
    assert trip.updated_at > today


def test_delete_point_touches_trip(app_client, db_session, session_user):
    created_at = dt.datetime.utcnow() - dt.timedelta(days=3)
    today = dt.datetime.combine(dt.date.today(), dt.time())

    trip = TripFactory(author=session_user, created_at=created_at, updated_at=created_at)
    point = PointFactory(trip=trip, type=PointTypes.ENTERTAINMENT.value)
    db_session.add(trip)
    db_session.add(point)
    db_session.commit()

    with app_client.session_transaction() as session:
        session['user_id'] = session_user.id

    res = app_client.post(f'/trips/{trip.key}/{point.id}/delete')
    assert res.status_code in range(300, 400)

    db_session.refresh(trip)
    assert trip.created_at < today
    assert trip.updated_at > today
