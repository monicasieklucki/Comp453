from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, DateField, SelectField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError,Regexp
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flaskDemo import db, cursor
from flaskDemo.models import User #, Department, getDepartment, getDepartmentFactory
from wtforms.fields.html5 import DateField

# ssns = Department.query.with_entities(Department.mgr_ssn).distinct()
#  or could have used ssns = db.session.query(Department.mgr_ssn).distinct()
# for that way, we would have imported db from flaskDemo, see above


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class CheckoutForm(FlaskForm):
    def only_digits(form, field):
        if not field.data.isdecimal():
            raise ValidationError('Mobile number cannot contain letters.')

    customerEmail = StringField('Email', validators=[DataRequired(), Email()])
    customerPhone = StringField('Mobile' , validators=[DataRequired(), Length(10), only_digits])

    creditCardNum = StringField('Credit Card Number', validators=[DataRequired(), Length(16), only_digits])

    customerFirstName = StringField('First Name', validators=[DataRequired()])
    customerLastName = StringField('Last Name', validators=[DataRequired()])
    customerAddress = StringField('Address', validators=[DataRequired()])
    customerCity = StringField('City', validators=[DataRequired()])
    customerState = StringField('State', validators=[DataRequired(), Length(2)])
    customerZipCode = StringField('Zip Code', validators=[DataRequired(), Length(5), only_digits])


    submit = SubmitField('Place Your Order')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

class UpdateCustomerForm(FlaskForm):
    def only_digits(form, field):
        if not field.data.isdecimal():
            raise ValidationError('Mobile number cannot contain letters.')
    customerId = IntegerField('Id')
    customerPhone = StringField('Mobile', validators=[DataRequired(), Length(10), only_digits])
    customerFirstName = StringField('First Name', validators=[DataRequired()])
    customerLastName = StringField('Last Name', validators=[DataRequired()])
    customerAddress = StringField('Address', validators=[DataRequired()])
    customerCity = StringField('City', validators=[DataRequired()])
    customerState = StringField('State', validators=[DataRequired(), Length(2)])
    customerZipCode = StringField('Zip Code', validators=[DataRequired(), Length(5), only_digits])

    submit = SubmitField('Update')

#class UpdateAccountForm(FlaskForm):
#    username = StringField('Username',
#                           validators=[DataRequired(), Length(min=2, max=20)])
#    email = StringField('Email',
#                        validators=[DataRequired(), Email()])
#    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
#    submit = SubmitField('Update')

 #   def validate_username(self, username):
 #       if username.data != current_user.username:
 #           user = User.query.filter_by(username=username.data).first()
 #           if user:
 #               raise ValidationError('That username is taken. Please choose a different one.')

 #   def validate_email(self, email):
 #       if email.data != current_user.email:
 #           user = User.query.filter_by(email=email.data).first()
 #           if user:
 #               raise ValidationError('That email is taken. Please choose a different one.')

#class PostForm(FlaskForm):
#    title = StringField('Title', validators=[DataRequired()])
#    content = TextAreaField('Content', validators=[DataRequired()])
#    submit = SubmitField('Post')
   
#class DeptUpdateForm(FlaskForm):

#    dnumber=IntegerField('Department Number', validators=[DataRequired()])
#    dnumber = HiddenField("")

#    dname=StringField('Department Name:', validators=[DataRequired(),Length(max=15)])
#  Commented out using a text field, validated with a Regexp.  That also works, but a hassle to enter ssn.
#    mgr_ssn = StringField("Manager's SSN", validators=[DataRequired(),Regexp('^(?!000|666)[0-8][0-9]{2}(?!00)[0-9]{2}(?!0000)[0-9]{4}$', message="Please enter 9 digits for a social security.")])

#  One of many ways to use SelectField or QuerySelectField.  Lots of issues using those fields!!
#    mgr_ssn = SelectField("Manager's SSN", choices=myChoices)  # myChoices defined at top
    
# the regexp works, and even gives an error message
#    mgr_start=DateField("Manager's Start Date:  yyyy-mm-dd",validators=[Regexp(regex)])
#    mgr_start = DateField("Manager's Start Date")

#    mgr_start=DateField("Manager's Start Date", format='%Y-%m-%d')
#    mgr_start = DateField("Manager's start date:", format='%Y-%m-%d')  # This is using the html5 date picker (imported)
#    submit = SubmitField('Update this department')


# got rid of def validate_dnumber

#    def validate_dname(self, dname):    # apparently in the company DB, dname is specified as unique
#         dept = Department.query.filter_by(dname=dname.data).first()
#         if dept and (str(dept.dnumber) != str(self.dnumber.data)):
#             raise ValidationError('That department name is already being used. Please choose a different name.')


#class DeptForm(DeptUpdateForm):

#    dnumber=IntegerField('Department Number', validators=[DataRequired()])
#    submit = SubmitField('Add this department')

#    def validate_dnumber(self, dnumber):    #because dnumber is primary key and should be unique
#        dept = Department.query.filter_by(dnumber=dnumber.data).first()
#        if dept:
#            raise ValidationError('That department number is taken. Please choose a different one.')

