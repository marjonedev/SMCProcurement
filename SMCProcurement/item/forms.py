# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, HiddenField, DecimalField
from wtforms.fields import SelectField, TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, Email, DataRequired
from wtforms.widgets.html5 import NumberInput

from SMCProcurement import db

## login and registration

class ItemForm(FlaskForm):
    name = TextField('Name', id="name", validators=[DataRequired()])
    category_id = SelectField('Category', id="category_id", validators=[DataRequired()])
    supplier_id = SelectField('Supplier', id="supplier_id", validators=[DataRequired()])
    item_code = TextField('Item Code', id="item_code")
    serial = TextField('Serial', id="serial")
    brand = TextField('Brand', id="brand")
    model = TextField('Model', id="model")
    description = TextField('Description', id="description")
    unit_price = DecimalField("Unit Price", id="unit_price", widget=NumberInput(step="any"), default=0.00)
