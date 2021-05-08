from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, HiddenField, FieldList, FormField, DecimalField, IntegerField, \
    SubmitField, StringField
from wtforms.fields import SelectField, DateField
from wtforms.validators import InputRequired, Email, DataRequired
from wtforms.widgets.html5 import NumberInput

class InventoryItemForm(FlaskForm):
    class Meta:
        csrf = False

    item_id = TextField("Item Id")
    qty = IntegerField("Quantity", widget=NumberInput())
    purchased_date = TextField("Purchased Date")


class InventoryForm(FlaskForm):
    class Meta:
        csrf = False

    submit = SubmitField('Submit')
    inventory_items = FieldList(FormField(InventoryItemForm))