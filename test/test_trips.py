from flask import url_for
from bs4 import BeautifulSoup
from werkzeug.test import TestResponse

from trip_planner.models import PrivacyStatusEnum
from test.factories import TripFactory, UserFactory


def _find_links_with_path(response: TestResponse, subpath: str):
    html = response.get_data(as_text=True)
    soup = BeautifulSoup(html)
    return [a for a in soup.find_all('a') if subpath in a.get('href')]


def test_shows_my_trip(session_user, db_session, app_client):
    trip = TripFactory(author=session_user)
    with app_client.session_transaction() as session:
        session['user_id'] = session_user.id

    response = app_client.get(url_for('trips.show', slug=trip.slug), follow_redirects=True)
    assert response.status_code == 200
    assert trip.slug in response.request.path
    assert _find_links_with_path(response, 'update')


def test_doesn_show_others_private_trip(session_user, db_session, app_client):
    other_user = UserFactory()
    trip = TripFactory(author=other_user)

    with app_client.session_transaction() as session:
        session['user_id'] = session_user.id

    response = app_client.get(url_for('trips.show', author_id=other_user.username, slug=trip.slug), follow_redirects=True)
    assert response.status_code == 403


def test_shows_others_public_trip(session_user, db_session, app_client):
    other_user = UserFactory()
    with db_session.begin_nested():
        trip = TripFactory.build(author=other_user, privacy_status=PrivacyStatusEnum.public, points_count=3)
        point = trip.points[0]
        point.privacy_status = PrivacyStatusEnum.public

    with app_client.session_transaction() as session:
        session['user_id'] = session_user.id

    response = app_client.get(url_for('trips.show', author_id=other_user.username, slug=trip.slug), follow_redirects=True)
    assert response.status_code == 200
    assert trip.slug in response.request.path
    assert not _find_links_with_path(response, 'update')
    assert BeautifulSoup(response.get_data(as_text=True)).find('li', class_='trip-point-item')
