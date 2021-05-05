from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, HiddenField, FieldList, FormField, DecimalField, IntegerField, \
    SubmitField, StringField
from wtforms.fields import SelectField, DateField
from wtforms.validators import InputRequired, Email, DataRequired
from wtforms.widgets.html5 import NumberInput

class InventoryForm(FlaskForm):
    request_id = SelectField('Request', id="request_id", validators=[DataRequired()])
    submit = SubmitField('Submit')