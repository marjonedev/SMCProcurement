# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, HiddenField, DecimalField, FieldList, FormField, StringField
from wtforms.fields import SelectField, TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, Email, DataRequired
from wtforms.widgets.html5 import NumberInput

from SMCProcurement import db

## login and registration
class InventoryReportForm(FlaskForm):
    class Meta:
        csrf = False
    report_by = SelectField('Name', id="report_by", choices=[(1, "All Items"), (2, "Departments")])
    start_date = HiddenField('Start Date')
    end_date = HiddenField('End Date')

class InventoryItemPrintForm(FlaskForm):
    class Meta:
        csrf = False
    remarks = StringField("Remarks")
    id = HiddenField('ID')

class InventoryPrintForm(FlaskForm):
    class Meta:
        csrf = False

    start_date = HiddenField('Start Date')
    end_date = HiddenField('End Date')
    report_by = HiddenField('Report By')
    inventory_items = FieldList(FormField(InventoryItemPrintForm))

class RequestReportForm(FlaskForm):
    class Meta:
        csrf = False
    report_by = SelectField('Name', id="report_by", choices=[(1, "All Items"), (2, "Departments")])
    start_date = HiddenField('Start Date')
    end_date = HiddenField('End Date')

class RequestItemPrintForm(FlaskForm):
    class Meta:
        csrf = False
    remarks = StringField("Remarks")
    id = HiddenField('ID')

class RequestPrintForm(FlaskForm):
    class Meta:
        csrf = False

    start_date = HiddenField('Start Date')
    end_date = HiddenField('End Date')
    report_by = HiddenField('Report By')
    request_items = FieldList(FormField(RequestItemPrintForm))

