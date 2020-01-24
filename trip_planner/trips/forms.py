from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, SelectField
from wtforms.validators import DataRequired, Length, Optional, Regexp, NoneOf


class TripForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=2000)])
    country_code = StringField('Country code',
                               validators=[Optional(strip_whitespace=True),
                                           Length(min=2, max=2)])
    slug = StringField('Slug',
                       validators=[DataRequired(), Length(min=3, max=2000),
                                   Regexp(r'\w[\w_-]*\w'),
                                   NoneOf(['new', 'update', 'delete'])])


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
