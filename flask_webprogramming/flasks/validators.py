from wtforms import Form, BooleanField, TextField, PasswordField, validators, StringField, Field


class RegistrationForm(Form):
    userid = TextField('SV.userid', [validators.Length(min=5, max=13)], id='useris')
    username = TextField('SV.username', [validators.Length(min=4)])
    password1 = PasswordField('SV.password1', [validators.DataRequired(), validators.EqualTo('password2', message='Server: Password1과 Password2가 다릅니다.')])
    password2 = PasswordField('SV.password2', [validators.DataRequired()])
    # mail = TextField('SV.mail', [validators.Email(message='not is valid'), validators.Length(min=6, max=35)])
    # phoneNumber = TextField('SV.phoneNumber', [validators.Regexp('([0-9])', message='Server: only numbers.')])
    
