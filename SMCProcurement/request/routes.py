from SMCProcurement.request import blueprint
from flask import render_template, redirect, url_for, request, flash, session
from flask_login import login_required, current_user
from SMCProcurement import login_manager
from jinja2 import TemplateNotFound
from SMCProcurement.models import Department
from SMCProcurement.models import Request
from SMCProcurement.models.request_type import RequestType
from SMCProcurement import db
from SMCProcurement.enum.user_type import UserTypeEnum
from SMCProcurement.request.forms import CreateRequestForm
from SMCProcurement.user.util import roles_accepted
from pprint import pprint

from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user
)



@blueprint.route('/requests')
@login_required
@roles_accepted([UserTypeEnum.administrator, UserTypeEnum.president, UserTypeEnum.vpfinance])
def all_requests():
    requests = db.session.query(Request).all()

    return render_template('requests/index.html', requests=requests)

@blueprint.route('/requests/mine')
@login_required
def my_requests():
    requests = db.session.query(Request).filter(Request.user_id == current_user.id).all()

    return render_template('requests/index.html', requests=requests)


@blueprint.route('/requests/academic')
@login_required
@roles_accepted([UserTypeEnum.administrator,
                 UserTypeEnum.president,
                 UserTypeEnum.vpfinance,
                 UserTypeEnum.vpacad])
def academic_requests():
    types = db.session.query(RequestType).filter(RequestType.user_type == UserTypeEnum.vpacad.value).all()
    requests = db.session.query(Request).filter(Request.request_type_id in [t.id for t in types]).all()

    return render_template('requests/index.html', requests=requests)


@blueprint.route('/requests/admin')
@login_required
@roles_accepted([UserTypeEnum.administrator,
                 UserTypeEnum.president,
                 UserTypeEnum.vpfinance,
                 UserTypeEnum.vpadmin])
def admin_requests():
    types = db.session.query(RequestType).filter(RequestType.user_type == UserTypeEnum.vpadmin.value).all()
    requests = db.session.query(Request).filter(Request.request_type_id in [t.id for t in types]).all()

    return render_template('requests/index.html', requests=requests)


@blueprint.route('/requests/create')
@login_required
def create_request():
    createRequestForm = CreateRequestForm(request.form)
    createRequestForm.department_id.choices = [(d.id, d.name) for d in Department.query.all()]
    createRequestForm.department_id.default = current_user.department_id
    createRequestForm.process()
    return render_template('requests/create.html', form=createRequestForm)