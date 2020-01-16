from itertools import groupby
from operator import attrgetter
from flask import Blueprint, g, render_template, redirect, url_for
from flask.views import MethodView as View
from sqlalchemy.exc import IntegrityError
import psycopg2.errorcodes as pgerrorcodes

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


class TripCUView(View):
    methods = ('GET', 'POST')
    decorators = [user_required]
    title = 'Trip action'
    submit_text = 'Save'

    def dispatch_request(self, *args, **kwargs):
        self.model = self._instant_model()
        return super().dispatch_request(*args, **kwargs)

    def get(self):
        self.form = self._build_form()
        return self._default_render()

    def post(self):
        self.form = TripForm()
        if self.form.validate():
            try:
                self.form.populate_obj(self.model)
                db.session.add(self.model)
                db.session.commit()
                return redirect(url_for('.index'))
            except IntegrityError as e:
                db.session.rollback()
                if (e.orig.pgcode == pgerrorcodes.UNIQUE_VIOLATION):
                    self.form.errors.setdefault('slug', [])
                    self.form.errors['slug'].append('Already exists')
                    return self._default_render()
                else:
                    raise e
        return self._default_render()

    def _build_form(self):
        raise NotImplementedError

    def _instant_model(self) -> Trip:
        raise NotImplementedError

    def _default_render(self):
        return render_template('form.html', form=self.form,
                               title=self.title,
                               submit_text=self.submit_text)


class CreateTripView(TripCUView):
    title = 'Create trip'

    def _build_form(self):
        return TripForm()

    def _instant_model(self):
        return Trip(author=g.user)


class UpdateTripView(TripCUView):
    @property
    def title(self):
        return f"Updating {self.model.name}"

    def dispatch_request(self, slug):
        self.slug = slug
        return super().dispatch_request()

    def _build_form(self):
        return TripForm(obj=self.model)

    def _instant_model(self):
        return Trip.query\
                   .filter_by(slug=self.slug, author=g.user)\
                   .first_or_404()


trips.add_url_rule('/new', view_func=CreateTripView.as_view('new'))
trips.add_url_rule('/<slug>/update', view_func=UpdateTripView.as_view('update'))
