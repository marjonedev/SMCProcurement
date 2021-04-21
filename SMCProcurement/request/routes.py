from SMCProcurement.user import blueprint
from flask import render_template, redirect, url_for, request, flash, session
from flask_login import login_required, current_user
from SMCProcurement import login_manager
from jinja2 import TemplateNotFound
from SMCProcurement.models.user import User
from SMCProcurement.models.department import Department
from SMCProcurement.models.request_type import RequestType
from SMCProcurement.user.forms import UserForm
from SMCProcurement import db
from SMCProcurement.enum.user_type import UserTypeEnum

from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user
)

from pprint import pprint

@blueprint.route('/requests')
@login_required
def requests():
    return render_template('requests/index.html')

