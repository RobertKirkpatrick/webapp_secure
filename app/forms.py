from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()], id="uname")
    password = PasswordField('Password', validators=[DataRequired()], id="pword")
    # MFA optional to be added
    twofact = StringField('TwoFactor', id='2fa')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()], id="uname")
    password = PasswordField('Password', validators=[DataRequired()], id="pword")
    # password2 = PassworddField(
    #    'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    twofact = StringField('TwoFactor', id='2fa')
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')


class spellcheckForm(FlaskForm):
    spellcheck = StringField('Word', validators=[DataRequired()], id="inputtext")
    submit = SubmitField('spellcheck')