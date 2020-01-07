from itertools import groupby
from operator import attrgetter
from flask import Blueprint, g, render_template

from ..shared import user_requred
from ..models import Trip
from .data import TripsData

trips = Blueprint('trips', __name__, url_prefix='/trips',
                  template_folder='templates')


@trips.before_request
def add_data():
    g.trips_data = TripsData()


@trips.route("/")
@user_requred
def index():
    trips = Trip.query.filter_by(author_id=g.user.id)
    return render_template('index.html', trips=trips)


@trips.route("/<slug>")
@user_requred
def show(slug):
    trip = Trip.query.filter_by(author_id=g.user.id, slug=slug).first_or_404()
    points = groupby(trip.points, attrgetter('type'))
    return render_template('show.html', trip=trip, points=points,
                           view_class='show-trip',
                           map_url=g.trips_data.map_url)
