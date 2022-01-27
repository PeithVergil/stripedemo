from wtforms import Form, StringField, validators


class LoginForm(Form):

    username = StringField('Username', [
        validators.DataRequired(),
    ])

    password = StringField('Password', [
        validators.DataRequired(),
    ])

    remember = StringField('Remember', [
        validators.Optional(),
    ])


class RegistrationForm(Form):

    username = StringField('Username', [
        validators.DataRequired(),
    ])

    password = StringField('Password', [
        validators.DataRequired(),
    ])
