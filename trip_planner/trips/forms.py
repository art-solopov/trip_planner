from os.path import join as pjoin
import json
from collections import OrderedDict
from copy import copy

from flask_wtf import FlaskForm
from markupsafe import Markup, escape
from wtforms import (Form, StringField, TextAreaField, FloatField,
                     SelectField, HiddenField, FormField, FieldList)
from wtforms.widgets import html_params
from wtforms.utils import unset_value
from wtforms.validators import DataRequired, Length, Optional, Regexp, NoneOf

from trip_planner import DATA_PATH


class TripForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=2000)])
    country_code = SelectField('Country', choices=[],
                               validators=[Optional(strip_whitespace=True)])
    slug = StringField('Slug',
                       validators=[DataRequired(), Length(min=3, max=2000),
                                   Regexp(r'\w[\w_-]*\w'),
                                   NoneOf(['new', 'update', 'delete'])])

    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.country_code.choices = self._country_code_choices()

    def _country_code_choices(self):
        yield ('', '')
        file_name = pjoin(DATA_PATH, 'countries.json')
        with open(file_name) as f:
            for country in json.load(f):
                yield (country['Code'], country['Name'])


class ScheduleWidget:
    input_type = 'schedule'
    html_params = staticmethod(html_params)

    TABLE_CLASS = 'schedule-table'
    FORM_CLASS = 'schedule-table-form'

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        kwargs.setdefault('class_', '')

        html_class = set(kwargs['class_'].split(' '))
        html_class.add(self.TABLE_CLASS)
        html_class.add(self.FORM_CLASS)
        kwargs['class_'] = ' '.join(cls for cls in html_class if cls)

        return Markup(''.join(self.table_rows(field, **kwargs)))

    def table_rows(self, field, **kwargs):
        yield f'<table {self.html_params(**kwargs)}>'

        yield ('<thead>' +
               '<tr><th></th><th>From</th><th>To</th>' +
               "</thead>\n<tbody>")

        cell_class = f'{self.FORM_CLASS}--input-cell'

        for subfield in field:
            weekday = escape(subfield.weekday.data)

            yield ('<tr>' +
                   f'<td class={weekday}>{weekday.capitalize()}' +
                   f'{subfield.weekday()}</td>' +
                   f'<td class="{cell_class}">{subfield.open_from()}</td>' +
                   f'<td class="{cell_class}">{subfield.open_to()}</td>' +
                   '</tr>')

        yield "</tbody>\n</table>"


class ScheduleSubForm(Form):
    weekday = HiddenField()
    open_from = StringField('From', render_kw={'pattern': '\\d{1,2}:\\d{2}'})
    open_to = StringField('To', render_kw={'pattern': '\\d{1,2}:\\d{2}'})


class ScheduleField(FieldList):
    WEEKDAYS = 'mon tue wed thu fri sat sun'.split()
    widget = ScheduleWidget()

    def __init__(self, label=None, validators=None, **kwargs):
        default = [{'weekday': wday} for wday in self.WEEKDAYS]

        super().__init__(
            unbound_field=FormField(ScheduleSubForm),
            label=label,
            validators=validators,
            default=default,
            **kwargs
        )

    def process(self, formdata, data=unset_value):
        if isinstance(data, dict):
            data = [{**datum, 'weekday': wday}
                    for (wday, datum) in data.items()]

        print(data)
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
    TYPE_CHOICES = [
        ('museum', 'Museum'),
        ('sight', 'Sight'),
        ('transport', 'Transport'),
        ('accomodation', 'Accomodation'),
        ('food', 'Food'),
        ('entertainment', 'Entertainment'),
        ('shop', 'Shop'),
        ('other', 'Other'),
    ]

    name = StringField('Name', validators=[DataRequired(), Length(max=2000)])
    address = TextAreaField('Address')
    lat = FloatField('Latitude', validators=[DataRequired()])
    lon = FloatField('Longitude', validators=[DataRequired()])
    type = SelectField('Point type', choices=TYPE_CHOICES)
    notes = TextAreaField('Notes')
    schedule = ScheduleField('Schedule')

    # def process(self, formdata=None, obj=None, data=None, **kwargs):
    #     super().process(formdata, obj, data, **kwargs)

    #     current_weekdays = set(x.data['weekday'] for x in self.schedule)
    #     for wday in ScheduleSubForm.WEEKDAYS:
    #         if wday in current_weekdays:
    #             continue
    #         self.schedule.append_entry({'weekday': wday})
