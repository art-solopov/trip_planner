from functools import wraps
from itertools import groupby
from operator import attrgetter
from typing import Dict

from flask import (Blueprint, g, render_template,
                   request, redirect, url_for, flash,
                   make_response)
from flask.views import MethodView as View
from sqlalchemy.exc import IntegrityError
import psycopg2.errorcodes as pgerrorcodes
from markupsafe import escape

from .. import db
from ..shared import user_required, add_breadcrumb
from ..models import Trip, Point
from ..data import MapData
from .data import PointData
from .forms import TripForm, PointForm
from ..tailwind import (ViewClasses as TwViewClasses,
                        ScheduleClasses as TwScheduleClasses)
from ..bs_classes import ViewClasses, ScheduleClasses

trips = Blueprint('trips', __name__, url_prefix='/trips')


@trips.before_request
def add_data():
    g.map_data = MapData()


@trips.app_template_global()
def geocode_field_kwargs(field_name: str) -> Dict[str, str]:
    return {'data-geocode-target': field_name,
            'data-map-pointer-target': field_name,
            'data-action': 'change->map-pointer#moveMap'}


def _map_pointer_view_attrs() -> Dict[str, str]:
    return {
        'data-controller': 'map-pointer geocode',
        'data-map-pointer-apikey-value': g.map_data.api_key,
        'data-map-pointer-styleurl-value': g.map_data.MAPBOX_STYLE_URL
        }


@trips.route("/")
@user_required
def index():
    trips = g.user.trips
    response = make_response(render_template('trips/index.html', trips=trips))
    response.add_etag()
    return response.make_conditional(request)


@trips.route("/<slug>")
@user_required
def show(slug):
    trip = Trip.query.filter_by(author_id=g.user.id, slug=slug).first_or_404()
    points = groupby(trip.points, attrgetter('type'))

    add_breadcrumb('Trips', url_for('.index'))
    add_breadcrumb(trip.name)

    view_attrs = {
        'data-controller': 'map',
        'data-map-apikey-value': g.map_data.api_key,
        'data-map-styleurl-value': g.map_data.MAPBOX_STYLE_URL,
        'data-map-centerlat-value': trip.center_lat,
        'data-map-centerlon-value': trip.center_lon
    }

    response = make_response(
        render_template('trips/show.html', trip=trip,
                        points=points,
                        points_count=len(trip.points),
                        view_class=ViewClasses.TRIP_SHOW,
                        view_attrs=view_attrs))
    response.add_etag()

    return response.make_conditional(request)


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
                # Extracting the new model into the session
                model = db.session.merge(self.model)
                flash(self._success_flash_text(model), 'success')
                return redirect(url_for('.index'))
            except IntegrityError as e:
                db.session.rollback()
                if (e.orig.pgcode == pgerrorcodes.UNIQUE_VIOLATION):
                    self.form.errors.setdefault('slug', [])
                    self.form.errors['slug'].append('Already exists')
                    return self._default_render()
                else:
                    raise e
        db.session.rollback()
        return self._default_render()

    def _build_form(self):
        raise NotImplementedError

    def _instant_model(self) -> Trip:
        raise NotImplementedError

    def _default_render(self):
        self._add_breadcrumbs()
        add_breadcrumb(self.title)
        view_attrs = _map_pointer_view_attrs()
        return render_template('trips/form.html', form=self.form,
                               title=self.title,
                               view_attrs=view_attrs,
                               latlon=self._latlon(),
                               submit_text=self.submit_text)

    def _add_breadcrumbs(self):
        add_breadcrumb('Trips', url_for('.index'))

    def _success_flash_text(self, trip: Trip):
        return ''

    def _latlon(self):
        return None


class CreateTripView(TripCUView):
    title = 'Create trip'
    success_flash_text = 'Trip created'

    def _build_form(self):
        return TripForm()

    def _instant_model(self):
        return Trip(author=g.user)

    def _success_flash_text(self, trip: Trip):
        return f"Trip «{trip.name}» created"


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

    def _add_breadcrumbs(self):
        super()._add_breadcrumbs()
        add_breadcrumb(self.model.name, url_for('.show', slug=self.model.slug))

    def _success_flash_text(self, trip: Trip):
        return f"Trip «{trip.name}» updated"

    def _latlon(self):
        return (self.model.center_lat, self.model.center_lon)


@trips.route('/<slug>/delete', methods=('GET', 'POST'))
def delete_trip(slug: str):
    trip = Trip.query.filter_by(slug=slug).first_or_404()
    if request.method == 'POST':
        db.session.delete(trip)
        db.session.commit()
        flash(f"Trip «{trip.name}» deleted", 'success')
        return redirect(url_for('.index'))

    add_breadcrumb('Trips', url_for('.index'))
    add_breadcrumb(trip.name, url_for('.show', slug=trip.slug))
    add_breadcrumb('Delete')
    message = (f'Are you sure you want to delete trip {trip.name} ' +
               'and all its points?')
    return render_template('confirm_form.html', submit_label='Delete',
                           message=message)


trips.add_url_rule('/new', view_func=CreateTripView.as_view('new'))
trips.add_url_rule('/<slug>/update',
                   view_func=UpdateTripView.as_view('update'))

# Points CRUD


def weekday_class(weekday: str) -> str:
    weekday = escape(weekday)
    wday_short = weekday[0:3]
    weekday_classes = ScheduleClasses.WEEKDAYS
    return weekday_classes.get(wday_short, weekday_classes['_default'])


trips.add_app_template_filter(weekday_class, 'weekday_class')
trips.add_app_template_global(ScheduleClasses.CELL_CLASS,
                              'schedule_cell_class')
trips.add_app_template_global(ScheduleClasses.HEADER_CELL_CLASS,
                              'schedule_header_cell_class')
trips.add_app_template_global(ScheduleClasses.COMMON_WEEKDAY_CLASS,
                              'schedule_weekday_class')


def trip_point_wrapper(f):
    @wraps(f)
    def handler(slug: str, id: int):
        trip = Trip.query.filter_by(slug=slug).first_or_404()
        point = Point.query.filter(Point.trip == trip, Point.id == id)\
                           .first_or_404()

        add_breadcrumb('Trips', url_for('.index'))
        add_breadcrumb(trip.name, url_for('.show', slug=trip.slug))

        return f(trip, point)
    return handler


@trips.route("/<slug>/add-point", methods=('GET', 'POST'))
@user_required
def add_point(slug: str):
    trip = Trip.query.filter_by(slug=slug).first_or_404()
    point = Point(trip=trip)
    form = PointForm()
    if form.validate_on_submit():
        form.populate_obj(point)
        db.session.add(point)
        db.session.commit()
        flash(f"Point «{point.name}» added", 'success')
        return redirect(url_for('.show', slug=trip.slug))

    add_breadcrumb('Trips', url_for('.index'))
    add_breadcrumb(trip.name, url_for('.show', slug=trip.slug))
    add_breadcrumb('Add point')
    return render_template('points/form.html', form=form, point=point,
                           title='Add point',
                           view_attrs=_map_pointer_view_attrs(),
                           latlon=(trip.center_lat, trip.center_lon))


@trips.route("/<slug>/<int:id>")
@user_required
@trip_point_wrapper
def show_point(trip: Trip, point: Point):
    data = PointData(point)
    add_breadcrumb(point.name)
    response = make_response(render_template('points/show.html', point=point,
                             data=data, view_class=ViewClasses.POINT_SHOW))
    response.add_etag()
    return response.make_conditional(request)


@trips.route("/<slug>/<int:id>/update", methods=('GET', 'POST'))
@user_required
@trip_point_wrapper
def update_point(trip: Trip, point: Point):
    form = PointForm(obj=point)
    if form.validate_on_submit():
        form.populate_obj(point)
        db.session.add(point)
        db.session.commit()
        flash(f"Point «{point.name}» updated", 'success')
        return redirect(url_for('.show_point', slug=trip.slug, id=point.id))

    title = f'Update point {point.name}'
    add_breadcrumb(title)
    return render_template('points/form.html', form=form, point=point,
                           view_attrs=_map_pointer_view_attrs(),
                           latlon=(point.lat, point.lon),
                           title=title)


@trips.route("/<slug>/<int:id>/delete", methods=('GET', 'POST'))
@user_required
@trip_point_wrapper
def delete_point(trip: Trip, point: Point):
    if request.method == 'POST':
        db.session.delete(point)
        db.session.commit()
        flash(f"Point «{point.name}» deleted", 'success')
        return redirect(url_for('.show', slug=trip.slug))
    message = f'Are you sure you want to delete {point.name}?'
    return render_template('confirm_form.html', submit_label='Delete',
                           message=message)
