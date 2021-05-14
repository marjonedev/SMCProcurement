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
    report_by = SelectField('Name', id="report_by", choices=[(1, "All Items"), (2, "Departments")])
    start_date = HiddenField('Start Date', id="start_date")
    end_date = HiddenField('Start Date', id="end_date")

class InventoryItemPrintForm(FlaskForm):
    remarks = StringField("Remarks")
    id = HiddenField('ID')

class InventoryPrintForm(FlaskForm):
    inventory_items = FieldList(FormField(InventoryItemPrintForm))

