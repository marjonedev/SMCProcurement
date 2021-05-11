from datetime import date
from pprint import pprint

from SMCProcurement import db
from flask import render_template, redirect, url_for, request, flash, session, abort

from SMCProcurement.enum.request_status import RequestStatusEnum
from SMCProcurement.models import Inventory
from SMCProcurement.reports import blueprint
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user
)

@blueprint.route('/reports/inventory')
@login_required
def inventory_reports():
    return render_template('reports/inventory.html')

