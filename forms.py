from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, URL

class RegisterForm(FlaskForm):
    username = StringField("Username")
    email = StringField("Email")
    password = PasswordField("Password")
    submit = SubmitField("Submit")

class LoginForm(FlaskForm):
    email = StringField("Email")
    password = PasswordField("Password")
    submit = SubmitField("Login")


class CommentForm(FlaskForm):
    content = TextAreaField(render_kw={"placeholder": "Type in your text.",
                                       "class": "form-control"
                                       })
    send = SubmitField("Send", render_kw={"class": "btn btn-primary mb-3"})