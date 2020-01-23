from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, SelectField
from wtforms.validators import DataRequired, Length


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
