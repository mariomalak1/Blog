from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import EqualTo, Length, Email, DataRequired, ValidationError
from appname.users.models import User
from flask_login import current_user


class LoginForm(FlaskForm):
    custom_validators = [DataRequired()]
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField("Password",validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegistrationFrom(FlaskForm):
    username = StringField('User name', validators=[DataRequired(), Length(min= 2, max= 40)], render_kw={"placeholder": "mario_malak"})
    email = StringField('Email', validators=[Email(), DataRequired()], render_kw={"placeholder": "you@example.com"})
    password = PasswordField('password', validators=[DataRequired(),Length(min = 8, max = 50)] )
    password_confirmation = PasswordField('password confirmation', validators=[EqualTo('password')])
    submit = SubmitField("submit")

    def validate_email(self, email):
        user = User.query.filter_by(email= email.data).first()
        if user:
            raise ValidationError("this email is already taken please enter a different one")

    def validate_username(self, username):
        user = User.query.filter_by(username= username.data).first()
        if user:
            raise ValidationError("this user name is already taken please enter a different one")

class ChangeInformationForm(FlaskForm):
    username = StringField('User name', validators=[Length(min=2, max=40)],render_kw={})
    email = StringField('Email', validators=[Email()])
    image_name = FileField("Choose profile picture", validators= [ FileAllowed( [ 'jpg', 'png' ] ) ])
    submit = SubmitField("Change")

    def validate_email(self, email):
        user = User.query.filter_by(email= email.data).first()
        if (user and current_user.username != user.username):
            raise ValidationError("this email is already taken please enter a different one")


    def validate_username(self, username):
        user = User.query.filter_by(username= username.data).first()
        if (user and current_user.email != user.email):
            raise ValidationError("this username is already taken please enter a different one")



class ForgetPasswordForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Send Code")

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user is None:
            raise ValidationError("there's no account for this email, you must register first")

class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired(), Length(min = 8, max= 50)])
    password_confirmation = PasswordField('password confirmation', validators=[EqualTo('password')])
    submit = SubmitField("Save")

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField("Old Password", validators=[DataRequired()])
    new_password = PasswordField("New Password", validators=[DataRequired(), Length(min = 8, max= 50)])
    new_password_confirmation = PasswordField('password confirmation', validators=[EqualTo('new_password')])
    submit = SubmitField("Save")