from os.path import join as pjoin
import json
from collections import OrderedDict

from flask_wtf import FlaskForm
from wtforms import (Form, Field, StringField, TextAreaField, FloatField,
                     SelectField, HiddenField, FormField, FieldList)
import wtforms.widgets
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


class ScheduleSubForm(Form):
    weekday = HiddenField()
    open_from = StringField('From')
    open_to = StringField('To')


class ScheduleField(Field):
    widget = wtforms.widgets.ListWidget()
    WEEKDAYS = 'mon tue wed thu fri sat sun'.split()

    def __init__(
            self,
            label=None,
            validators=None,
            default=(),
            _prefix='',
            **kwargs
    ):
        super().__init__(label, validators, default=default, **kwargs)

        self._prefix = _prefix
        self.schedule_forms = OrderedDict(
            (wday, FormField(ScheduleSubForm).bind(
                form=None,
                name=f"{self.short_name}-{wday}",
                id=f"{self.id}-{wday}",
                prefix=self._prefix,
                default={'weekday': wday},
                _meta=self.meta
            ))
            for wday in self.WEEKDAYS
        )

        for (wday, form) in self.schedule_forms.items():
            form.process(None)

    def __iter__(self):
        return iter(self.schedule_forms.values())

    def __len__(self):
        return len(self.schedule_forms)

    def __getitem__(self, index):
        return self.schedule_forms.values()[index]



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
