from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email,EqualTo, ValidationError, Length
import sqlite3
class LoginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegisterationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    passwordrep = PasswordField('Repeat Password',validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField("Register")
    
    def validate_username(self, username):
        return ValidationError("Username Not Available")

    def validate_email(self,email):
        return ValidationError("Email ID already in use")

class PostForm(FlaskForm):
    post = TextAreaField('Say something', validators=[
        DataRequired(), Length(min=1, max=500)])
    submit = SubmitField('Submit')


class CommentForm(FlaskForm):
    comment = TextAreaField('Write a comment!', validators=[
        DataRequired(), Length(min=1, max=140)])
    submit = SubmitField('Submit')

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')
