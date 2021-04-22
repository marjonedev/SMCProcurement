# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField
from wtforms.fields import SelectField, DateField
from wtforms.validators import InputRequired, Email, DataRequired
from SMCProcurement.enum.user_type import UserTypeEnum
from SMCProcurement import db

## login and registration
class CreateRequestForm(FlaskForm):
    department_id = SelectField('Department', id="department", validators=[DataRequired()])
    date_needed = DateField('Date Needed', id="date_needed", validators=[DataRequired()])
