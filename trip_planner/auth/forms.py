from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, HiddenField
from wtforms.validators import DataRequired, Length, Regexp, ValidationError


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    redirect = HiddenField()


class PasswordChangeForm(FlaskForm):
    current_password = PasswordField('Current password', validators=[DataRequired()])
    new_password = PasswordField(
        'New password', validators=[
            DataRequired(),
            Length(min=8, max=70),
            Regexp(r'.*\d.*', message='must have a number'),
            ],
        description=('Your password should be 8-70 characters long '
                     'and have an uppercase letter, a lowercase letter and a number'
                     )
        )
    password_confirmation = PasswordField('Confirm password', validators=[DataRequired()])

    def validate_new_password(self, field):
        if not any(s.isupper() for s in field.data):
            raise ValidationError('must have an uppercase letter')
        if not any(s.islower() for s in field.data):
            raise ValidationError('must have a lowercase letter')

    def validate_password_confirmation(self, field):
        if field.data != self.new_password.data:
            raise ValidationError("Passwords don't match")
