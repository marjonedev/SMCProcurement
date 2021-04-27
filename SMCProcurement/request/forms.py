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
    description = StringField("Description")
    qty = IntegerField("Quantity", widget=NumberInput())
    unit_price = DecimalField("Unit Price", widget=NumberInput(step="any"))
    id = HiddenField("ID")

class RequestForm(FlaskForm):
    department_id = SelectField('Department', id="department_id", validators=[DataRequired()])
    date_needed = DateField('Date Needed', id="date_needed", validators=[DataRequired()])
    endorsed_by = StringField("Endorsed by", id="endorsed_by")
    request_lines = FieldList(FormField(RequestLineForm), min_entries=1)
    submit_request = SubmitField('Submit')

    # sy_start = TextField('SY From', id="sy_start", default=get_sy()["start"])
    # sy_end = TextField('SY To', id="sy_end", default=get_sy()["end"])
    # date_requested = DateField('Request Date', id="date_requested")
    # user_id = SelectField("Requisitor", id="user_id")
    # request_type_id = TextField("Request Type", id="request_type_id")

