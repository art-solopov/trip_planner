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
