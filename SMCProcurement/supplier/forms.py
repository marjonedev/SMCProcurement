# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, HiddenField
from wtforms.fields import SelectField, TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, Email, DataRequired

from SMCProcurement import db

## login and registration

class SupplierForm(FlaskForm):
    name = TextField('Name', id="name", validators=[DataRequired()])
    email = EmailField('Email', id="email", validators=[Email()])
    contact_person = TextField('Contact Person', id="contact_person")
    address = TextAreaField('address', id="address")
    phone = TextField('phone', id="phone")
