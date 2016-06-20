from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from flask import url_for

class SigninForm(Form):
    email = StringField('Email: ',validators=[Required(),Length(1,64), Email()])
    password = PasswordField("Password: ", validators=[Required()])
    remember_me = BooleanField("Keep me logged in <br /> <a href='/auth/forgetpassword'>Forget password</a>" )
    submit = SubmitField("LOG IN")

class SignupForm(Form):
    email = StringField("Email: ", validators=[Required(), Length(1,64), Email()] )
    username = StringField("Username: ", validators=[Required(), Length(1,16)])
    password = PasswordField("Password: ", validators=[Required(), EqualTo("password2", message="Check password equal")])
    password2 = PasswordField("Password confirm: ", validators=[Required()])
    submit = SubmitField("Sign Up")

class ChangeEmailForm(Form):
    email = StringField('Email: ', validators=[Required(), Length(1, 64), Email()])
    new_email = StringField('NewEmail: ', validators=[Required(), Length(1, 64), Email()])
    password = PasswordField("Password: ", validators=[Required()])
    submit = SubmitField("Change")

class ChangePasswordForm(Form):
    email = StringField('Email: ', validators=[Required(), Length(1, 64), Email()])
    old_password = PasswordField("Password confirm: ", validators=[Required()])
    password = PasswordField("NewPassword: ",
                             validators=[Required(), EqualTo("password2", message="Check password equal")])
    password2 = PasswordField("NewPassword confirm: ", validators=[Required()])
    submit = SubmitField("Change")

class ChangeUserDataForm(Form):
    age = StringField('Age: ')
    sex = RadioField('SEX:', choices=[('1','男'), ('0', '女')])
    home = StringField("Home: ")
    submit = SubmitField("Change")

class ForgetPasswordForm(Form):
    email = StringField("Email: ", validators=[Required(), Length(1,64), Email()])
    submit = SubmitField("Send email")

class ResetPasswordForm(Form):
    password = PasswordField("NewPassword: ",
                             validators=[Required(), EqualTo("password2", message="Check password equal")])
    password2 = PasswordField("NewPassword confirm: ", validators=[Required()])
    submit = SubmitField("Reset")
