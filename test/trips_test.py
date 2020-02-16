import unittest
from html.parser import HTMLParser

from . import WithLogin, db
from .factories import TripFactory, PointFactory


# TODO: replace with beautiful_soup?

class IndexParser(HTMLParser):
    trips_count = 0
    in_trips_list = False

    def handle_starttag(self, tag, attrs):
        if tag == 'ul' and ('class', 'trips') in attrs:
            self.in_trips_list = True
        elif tag == 'li' and self.in_trips_list:
            self.trips_count += 1

    def handle_endtag(self, tag):
        if tag == 'ul' and self.in_trips_list:
            self.in_trips_list = False


class ShowParser(HTMLParser):
    points_count = 0

    def handle_starttag(self, tag, attrs):
        if tag == 'li' and ('class', 'trip-point-item') in attrs:
            self.points_count += 1


class TripsTest(WithLogin, unittest.TestCase):
    trip_seeds_count = 10

    def setUp(self):
        super().setUp()
        self.trips = TripFactory.create_batch(self.trip_seeds_count,
                                              author=self.user)

        for trip in self.trips:
            db.session.add(trip)
        db.session.flush()

    def test_index(self):
        res = self.client.get('/trips', follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        parser = IndexParser()
        parser.feed(res.data.decode('utf-8'))
        self.assertEqual(parser.trips_count, self.trip_seeds_count)

    def test_show(self):
        trip = self.trips[3]
        points = PointFactory.create_batch(5, trip=trip)
        for p in points:
            db.session.add(p)
        db.session.flush()
        res = self.client.get(f'/trips/{trip.slug}', follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        parser = ShowParser()
        parser.feed(res.data.decode('utf-8'))
        self.assertEqual(parser.points_count, len(points))
