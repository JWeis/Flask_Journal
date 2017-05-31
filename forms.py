import datetime
from flask_wtf import Form
from wtforms import (StringField, PasswordField, DateField,
                     IntegerField, TextAreaField )
from wtforms.validators import (DataRequired, ValidationError, Email,
                                Length, EqualTo, Regexp)

from models import User


def user_exists(form, field):
    if User.select().where(User.username == field.data).exists():
        raise ValidationError("User already exits")


def email_exitst(form, field):
    if User.select().where(User.email == field.data).exists():
        raise ValidationError("User with email already exists")


class RegistrationForm(Form):
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Regexp(r'[a-zA-Z0-9_]+$',
                   message=("Username should be one word"
                            "with letters, numbers and underscores"
                            "only. Please try again.")),
            user_exists
        ])
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(),
            email_exitst
        ])
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=2),
            EqualTo('password2', message='Passwords must match')
        ])
    password1 = PasswordField(
        'Confirm Password',
        validators=[DataRequired()])


class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])


class EntryForm(Form):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Entry', validators=[DataRequired()])
    date = DateField('Entry Date', validators=[DataRequired()])
    resources = TextAreaField('Resourses Remember')
    time_spent = IntegerField('Time Spent in Minutes',
                              validators=[DataRequired()])
    tags = StringField('Tags')