from itertools import groupby
from operator import attrgetter
from flask import Blueprint, g, render_template, redirect, url_for

from .. import db
from ..shared import user_required
from ..models import Trip
from ..data import MapData
from .forms import TripForm

trips = Blueprint('trips', __name__, url_prefix='/trips')


@trips.before_request
def add_data():
    g.map_data = MapData()


@trips.route("/")
@user_required
def index():
    trips = Trip.query.filter_by(author_id=g.user.id)
    return render_template('trips/index.html', trips=trips)


@trips.route("/<slug>")
@user_required
def show(slug):
    trip = Trip.query.filter_by(author_id=g.user.id, slug=slug).first_or_404()
    points = groupby(trip.points, attrgetter('type'))
    return render_template('trips/show.html', trip=trip, points=points,
                           view_class='show-trip',
                           map_url=g.map_data.map_url)


@trips.route("/new", methods=('GET', 'POST'))
@user_required
def new():
    form = TripForm()
    if form.validate_on_submit():
        model = Trip(author_id=g.user.id)
        form.populate_obj(model)
        db.session.add(model)
        db.session.commit()
        return redirect(url_for('.index'))
    print(form.errors)
    return render_template('form.html', form=form, submit_text='Create trip')
