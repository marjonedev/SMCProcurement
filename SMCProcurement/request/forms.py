# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, HiddenField, FieldList, FormField, DecimalField, IntegerField, \
    SubmitField, StringField
from wtforms.fields import SelectField, DateField
from wtforms.validators import InputRequired, Email, DataRequired
from wtforms.widgets.html5 import NumberInput

from SMCProcurement.base.util import get_sy
from SMCProcurement.enum.user_type import UserTypeEnum
from SMCProcurement import db

## login and registration
class RequestLineForm(FlaskForm):
    qty = IntegerField("Quantity", widget=NumberInput())
    unit_price = HiddenField("Unit Price")
    total = HiddenField("Total")
    id = HiddenField("ID")
    item_id = HiddenField("Item Id")

class RequestForm(FlaskForm):
    date_needed = DateField('Date Needed', id="date_needed", validators=[DataRequired()])
    request_type_id = SelectField('Request Type', id="request_type", validators=[DataRequired()])
    request_lines = FieldList(FormField(RequestLineForm), min_entries=1)
    submit_request = SubmitField('Submit')

