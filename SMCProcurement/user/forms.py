# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, HiddenField
from wtforms.fields import SelectField
from wtforms.validators import InputRequired, Email, DataRequired
from SMCProcurement.enum.user_type import UserTypeEnum
from SMCProcurement import db

## login and registration

class UserForm(FlaskForm):
    first_name = TextField('First Name', id="first_name_create", validators=[DataRequired()])
    last_name = TextField('First Name', id="first_name_create", validators=[DataRequired()])
    username = TextField('Username', id='username_create' , validators=[DataRequired()])
    email = TextField('Email', id='email_create', validators=[DataRequired(), Email()])
    password = PasswordField('Password' , id='pwd_create', validators=[DataRequired()])
    position = TextField('Position', id="position_create")
    department_id = SelectField('Department', id="department_create", validators=[DataRequired()])
    user_type = SelectField('User Type', id="user_type_create", choices=[(t.value, t.description) for t in UserTypeEnum], validators=[DataRequired()], default=UserTypeEnum.requisitor)
    request_type_id = SelectField('Request Type', id="request_type_create", validators=[DataRequired()])

class UserFormIndividual(FlaskForm):
    first_name = TextField('First Name', id="first_name_create", validators=[DataRequired()])
    last_name = TextField('First Name', id="first_name_create", validators=[DataRequired()])
    username = TextField('Username', id='username_create')
    email = TextField('Email', id='username_create')
    password = PasswordField('Password', id='pwd_create', validators=[DataRequired()])
    position = TextField('Position', id="position_create")
    department_id = SelectField('Department', id="department_create", validators=[DataRequired()])
