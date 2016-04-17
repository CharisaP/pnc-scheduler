
from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class MessageForm(Form):
    title = TextField('Title', validators=[DataRequired()])
    description = TextField(
        'Description', validators=[DataRequired()])

class RegisterForm(Form):
    username = TextField(
        'username',
        validators=[DataRequired(), Length(min=3, max=25)]
    )
    first_name = TextField(
        'first_name',
        validators=[DataRequired(), Length(min=6, max=40)]
    )
    last_name = TextField(
        'last_name',
        validators=[DataRequired(), Length(min=6, max=40)]
    )
    password = PasswordField(
        'password',
        validators=[DataRequired(), Length(min=6, max=25)]
    )
    confirm = PasswordField(
        'Repeat password',
        validators=[
            DataRequired(), EqualTo('password', message='Passwords must match.')
        ]
    )