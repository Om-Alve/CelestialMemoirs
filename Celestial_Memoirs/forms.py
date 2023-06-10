from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField, BooleanField, ValidationError, DateField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, Optional
from Celestial_Memoirs.models import Users
import datetime


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign in')
    remember = BooleanField('Remember me', default=True)


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')

    def validate_username(self, username):
        user = Users.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class PostForm(FlaskForm):
    date = DateField('Date', format='%Y-%m-%d', validators=[])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Add to your Space')

    def validate_date(self, date):
        live_date = datetime.date.today()
        if date.data and date.data > live_date:
            raise ValidationError('Invalid date. Please choose a date less than or equal to the current date.')
