from os.path import join as pjoin
import json
from copy import copy

from flask_wtf import FlaskForm
from wtforms import (Form, StringField, TextAreaField, FloatField,
                     SelectField, HiddenField, FormField, FieldList,
                     DecimalField, URLField)
from wtforms.widgets import TimeInput
from wtforms.utils import unset_value
from wtforms.validators import DataRequired, Length, Optional

from trip_planner import DATA_PATH
from .data import PointScheduleData
from ..models import PointTypes


class TripForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=2000)])
    country_code = SelectField('Country', choices=[],
                               validators=[Optional(strip_whitespace=True)])
    center_lat = DecimalField('Center latitude', places=5)
    center_lon = DecimalField('Center longitude', places=5)

    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.country_code.choices = list(self._country_code_choices())

    def _country_code_choices(self):
        yield ('', '')
        file_name = pjoin(DATA_PATH, 'countries.json')
        with open(file_name) as f:
            for country in json.load(f):
                yield (country['Code'], country['Name'])


class ScheduleSubForm(Form):
    weekday = HiddenField()
    open_from = StringField('From', widget=TimeInput())
    open_to = StringField('To', widget=TimeInput())


class ScheduleField(FieldList):
    WEEKDAYS = PointScheduleData.WEEKDAYS

    def __init__(self, label=None, validators=None, **kwargs):
        default = [{'weekday': wday} for wday in self.WEEKDAYS]

        super().__init__(
            unbound_field=FormField(ScheduleSubForm),
            label=label,
            validators=validators,
            default=default,
            **kwargs
        )

    def process(self, formdata, data=unset_value, extra_filters=None):
        if isinstance(data, dict):
            data = [{**datum, 'weekday': wday}
                    for (wday, datum) in data.items()]

        super().process(formdata, data)

    def populate_obj(self, obj, name):
        data = dict(self._transform_data(datum) for datum in self.data)
        setattr(obj, name, data)

    @staticmethod
    def _transform_data(dct: dict):
        dct = copy(dct)
        weekday = dct.pop('weekday')
        return (weekday, dct)


class PointForm(FlaskForm):
    TYPE_CHOICES = [(p.value, p.value.capitalize()) for p in PointTypes]

    name = StringField('Name', validators=[DataRequired(), Length(max=2000)])
    address = TextAreaField('Address')
    lat = FloatField('Latitude', validators=[DataRequired()])
    lon = FloatField('Longitude', validators=[DataRequired()])
    type = SelectField('Point type', choices=TYPE_CHOICES)
    websites = FieldList(URLField('Website'), min_entries=1, max_entries=20)
    notes = TextAreaField('Notes')
    schedule = ScheduleField('Schedule')
