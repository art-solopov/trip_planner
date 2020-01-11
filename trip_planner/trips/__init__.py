from itertools import groupby
from operator import attrgetter
from flask import Blueprint, g, render_template

from ..shared import user_requred
from ..models import Trip
from ..data import MapData

trips = Blueprint('trips', __name__, url_prefix='/trips')


@trips.before_request
def add_data():
    g.map_data = MapData()


@trips.route("/")
@user_requred
def index():
    trips = Trip.query.filter_by(author_id=g.user.id)
    return render_template('trips/index.html', trips=trips)


@trips.route("/<slug>")
@user_requred
def show(slug):
    trip = Trip.query.filter_by(author_id=g.user.id, slug=slug).first_or_404()
    points = groupby(trip.points, attrgetter('type'))
    return render_template('trips/show.html', trip=trip, points=points,
                           view_class='show-trip',
                           map_url=g.map_data.map_url)
