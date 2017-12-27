from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField, ValidationError, FileField
from wtforms.validators import DataRequired, Length, Email, Regexp
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from ..models import Role, User
from flask import request


class EditProfileForm(FlaskForm):
    name = StringField('Real name', validators=[Length(0, 64)])
    head_portrait = FileField('Upload your head portrait.(Within 1MB)', validators=[])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')


class EditProfileAdminForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    username = StringField('Username', validators=[DataRequired(), Length(1, 64),
                                                   Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                          'Username must have only letters,'
                                                          'numbers,dots or underscores')])
    head_portrait = FileField('Upload your head portrait.', validators=[])
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role', coerce=int)
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if field.data != self.user.username and User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already registered.')


'''
    def validate_head_portrait(self, field):
        if request.files['head_portrait']
            raise ValidationError('Email already registered.')
        '''
