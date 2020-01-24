from flask_wtf import FlaskForm
from wtforms import StringField, RadioField
from wtforms.validators import Optional


class GeocodeForm(FlaskForm):
    name = StringField(validators=[Optional()])
    address = StringField(validators=[Optional()])
    field = RadioField(choices=[('name', 'By name'),
                                ('address', 'By address'),])
