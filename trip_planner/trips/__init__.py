from functools import wraps
from itertools import groupby
from operator import attrgetter
from typing import Dict

from flask import (Blueprint, g, render_template,
                   request, redirect, url_for, flash,
                   make_response)
from flask.views import MethodView as View
from markupsafe import escape
from werkzeug.local import LocalProxy

from .. import db
from ..shared import user_required, add_breadcrumb
from ..models import Trip, Point
from ..data import MapData
from .data import PointData
from .forms import TripForm, PointForm
from .policy import Policy
from .presenters import TripPresenter, PointPresenter
from ..bs_classes import ViewClasses, ScheduleClasses

trips = Blueprint('trips', __name__, url_prefix='/trips')


# TODO: rewrite into local proxy maybe
@trips.before_request
def add_data():
    g.map_data = MapData()


def _get_policy():
    if 'policy' not in g:
        if g.user:
            g.policy = Policy(g.user)
    return g.policy


policy: Policy = LocalProxy(_get_policy)


@trips.app_template_global()
def geocode_field_kwargs(field_name: str) -> Dict[str, str]:
    return {'data-geocode-target': field_name,
            'data-map-pointer-target': field_name,
            'data-action': 'change->map-pointer#moveMap'}


def _map_pointer_view_attrs(map_pointer_mode) -> Dict[str, str]:
    return {
        'data-controller': 'map-pointer geocode',
        'data-map-pointer-apikey-value': g.map_data.api_key,
        'data-map-pointer-styleurl-value': g.map_data.MAPBOX_STYLE_URL,
        'data-map-pointer-mode-value': map_pointer_mode,
        }


@trips.route("/")
@user_required
def index():
    trips = db.session.scalars(policy.trips_query().order_by(Trip.name))
    response = make_response(render_template('trips/index.html', trips=trips))
    response.add_etag()
    return response.make_conditional(request)


@trips.route("/<key>")
@user_required
def show(key):
    trip = db.first_or_404(policy.trips_query().filter_by(key=key))
    trip = TripPresenter(trip)
    points = [PointPresenter(p) for p in trip.points]
    points = groupby(points, attrgetter('type'))

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
            self.form.populate_obj(self.model)
            db.session.add(self.model)
            db.session.commit()
            # Extracting the new model into the session
            model = db.session.merge(self.model)
            flash(self._success_flash_text(model), 'success')
            return redirect(url_for('.index'))
        db.session.rollback()
        return self._default_render()

    def _build_form(self):
        raise NotImplementedError

    def _instant_model(self) -> Trip:
        raise NotImplementedError

    def _default_render(self):
        self._add_breadcrumbs()
        add_breadcrumb(self.title)
        view_attrs = _map_pointer_view_attrs('city')
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
        # TODO: extract into constant
        return (51.48, 0)


class CreateTripView(TripCUView):
    title = 'Create trip'
    success_flash_text = 'Trip created'
    submit_text = 'Create trip'

    def _build_form(self):
        return TripForm()

    def _instant_model(self):
        return Trip(author=g.user)

    def _success_flash_text(self, trip: Trip):
        return f"Trip «{trip.name}» created"


class EditTripView(TripCUView):
    submit_text = 'Save changes'

    @property
    def title(self):
        return f"Editing {self.model.name}"

    def dispatch_request(self, key):
        self.key = key
        return super().dispatch_request()

    def _build_form(self):
        return TripForm(obj=self.model)

    def _instant_model(self):
        trip = db.first_or_404(db.select(Trip).filter_by(author=g.user, key=self.key))
        policy.authorize('edit_trip', trip)
        return trip

    def _add_breadcrumbs(self):
        super()._add_breadcrumbs()
        add_breadcrumb(self.model.name, url_for('.show', key=self.model.key))

    def _success_flash_text(self, trip: Trip):
        return f"Trip «{trip.name}» updated"

    def _latlon(self):
        return (self.model.center_lat, self.model.center_lon)


@trips.route('/<key>/delete', methods=('GET', 'POST'))
def delete_trip(key: str):
    trip = db.first_or_404(db.select(Trip).filter_by(author=g.user, key=key))
    policy.authorize('delete_trip', trip)
    if request.method == 'POST':
        db.session.delete(trip)
        db.session.commit()
        flash(f"Trip «{trip.name}» deleted", 'success')
        return redirect(url_for('.index'))

    add_breadcrumb('Trips', url_for('.index'))
    add_breadcrumb(trip.name, url_for('.show', key=trip.key))
    add_breadcrumb('Delete')
    message = (f'Are you sure you want to delete trip {trip.name} ' +
               'and all its points?')
    return render_template('confirm_form.html', submit_label='Delete',
                           message=message)


trips.add_url_rule('/new', view_func=CreateTripView.as_view('new'))
trips.add_url_rule('/<key>/edit',
                   view_func=EditTripView.as_view('edit'))

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
    def handler(key: str, id: int):
        trip = db.first_or_404(policy.trips_query().filter_by(key=key))
        point = db.first_or_404(policy.points_query(trip).filter_by(id=id))

        add_breadcrumb('Trips', url_for('.index'))
        add_breadcrumb(trip.name, url_for('.show', key=trip.key))

        return f(trip, point)
    return handler


@trips.route("/<key>/add-point", methods=('GET', 'POST'))
@user_required
def add_point(key: str):
    trip = db.first_or_404(policy.trips_query().filter_by(key=key))
    policy.authorize('add_point', trip)
    point = Point(trip=trip)
    form = PointForm()
    if form.validate_on_submit():
        form.populate_obj(point)
        db.session.add(point)
        db.session.commit()
        flash(f"Point «{point.name}» added", 'success')
        return redirect(url_for('.show', key=trip.key))

    add_breadcrumb('Trips', url_for('.index'))
    add_breadcrumb(trip.name, url_for('.show', key=trip.key))
    add_breadcrumb('Add point')
    return render_template('points/form.html', form=form, point=point,
                           title='Add point',
                           view_attrs=_map_pointer_view_attrs('point'),
                           latlon=(trip.center_lat, trip.center_lon))


@trips.route("/<key>/<int:id>")
@user_required
@trip_point_wrapper
def show_point(trip: Trip, point: Point):
    data = PointData(point)
    add_breadcrumb(point.name)
    response = make_response(render_template('points/show.html', point=point,
                             data=data, view_class=ViewClasses.POINT_SHOW))
    response.add_etag()
    return response.make_conditional(request)


@trips.route("/<key>/<int:id>/edit", methods=('GET', 'POST'))
@user_required
@trip_point_wrapper
def edit_point(trip: Trip, point: Point):
    policy.authorize('edit_point', point)
    form = PointForm(obj=point)
    if form.validate_on_submit():
        form.populate_obj(point)
        db.session.add(point)
        db.session.commit()
        flash(f"Point «{point.name}» updated", 'success')
        return redirect(url_for('.show_point', key=trip.key, id=point.id))

    title = f'Edit point {point.name}'
    add_breadcrumb(title)
    return render_template('points/form.html', form=form, point=point,
                           view_attrs=_map_pointer_view_attrs('point'),
                           latlon=(point.lat, point.lon),
                           title=title)


@trips.route("/<key>/<int:id>/delete", methods=('GET', 'POST'))
@user_required
@trip_point_wrapper
def delete_point(trip: Trip, point: Point):
    policy.authorize('delete_point', point)
    if request.method == 'POST':
        db.session.delete(point)
        db.session.commit()
        flash(f"Point «{point.name}» deleted", 'success')
        return redirect(url_for('.show', key=trip.key))
    message = f'Are you sure you want to delete {point.name}?'
    return render_template('confirm_form.html', submit_label='Delete',
                           message=message)


@trips.route("/<key>/<int:id>/buttons_row", methods=('GET',))
@user_required
@trip_point_wrapper
def buttons_row(trip: Trip, point: Point):
    return render_template('points/button_row.html', trip=trip, point=point)
