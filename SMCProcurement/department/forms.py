# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, HiddenField
from wtforms.fields import SelectField
from wtforms.validators import InputRequired, Email, DataRequired
from SMCProcurement import db

## login and registration

class DepartmentForm(FlaskForm):
    name = TextField('Name', id="name", validators=[DataRequired()])
    description = TextField('Description', id="description")
