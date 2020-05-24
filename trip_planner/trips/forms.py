from os.path import join as pjoin
import json

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, SelectField
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
    schedule = TextAreaField('Schedule')
