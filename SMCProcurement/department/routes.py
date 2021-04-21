from SMCProcurement.user import blueprint
from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user
from SMCProcurement import login_manager
from jinja2 import TemplateNotFound
from SMCProcurement.models.department import Department

@blueprint.route('/departments')
@login_required
def departments():
    departments = Department.query.all()
    return render_template('departments/index.html', departments=departments)