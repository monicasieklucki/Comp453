from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskdemo.models import User


class RegistrationForm(FlaskForm):
    customer_name = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    customer_email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    customer_address = StringField('Address',
                           validators=[DataRequired(), Length(min=10, max=50)])
    customer_type = StringField('Type',
                           validators=[DataRequired(), Length(1)])
    customer_phone = StringField('Phone Number',
                           validators=[DataRequired(), Length(10)])

    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(customer_name=customer_name.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(customer_email=customer_email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    customer_email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
