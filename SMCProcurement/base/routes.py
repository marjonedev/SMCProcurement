# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from datetime import datetime

from flask import jsonify, render_template, redirect, request, url_for
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user
)

from SMCProcurement import db, login_manager
from SMCProcurement.base import blueprint
from SMCProcurement.base.forms import LoginForm, CreateAccountForm
from SMCProcurement.enum.request_status import RequestStatusEnum
from SMCProcurement.enum.user_type import UserTypeEnum
from SMCProcurement.models.user import User

from SMCProcurement.base.util import verify_pass
import pytz, tzlocal
from pytz import timezone


@blueprint.route('/')
def route_default():
    return redirect(url_for('base_blueprint.login'))

## Login & Registration

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if 'login' in request.form:
        
        # read form data
        username = request.form['username']
        password = request.form['password']

        # Locate user
        user = User.query.filter_by(username=username).first()
        
        # Check the password
        if user and verify_pass( password, user.password):

            login_user(user)
            return redirect(url_for('base_blueprint.route_default'))

        # Something (user or pass) is not ok
        return render_template( 'accounts/login.html', msg='Wrong user or password', form=login_form)

    if not current_user.is_authenticated:
        return render_template( 'accounts/login.html',
                                form=login_form)
    return redirect(url_for('home_blueprint.index'))

@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    login_form = LoginForm(request.form)
    create_account_form = CreateAccountForm(request.form)
    if 'register' in request.form:

        username  = request.form['username']
        email     = request.form['email'   ]

        # Check usename exists
        user = User.query.filter_by(username=username).first()
        if user:
            return render_template( 'accounts/register.html', 
                                    msg='Username already registered',
                                    success=False,
                                    form=create_account_form)

        # Check email exists
        user = User.query.filter_by(email=email).first()
        if user:
            return render_template( 'accounts/register.html', 
                                    msg='Email already registered', 
                                    success=False,
                                    form=create_account_form)

        # else we can create the user
        user = User(**request.form)
        db.session.add(user)
        db.session.commit()

        return render_template( 'accounts/register.html', 
                                msg='User created please <a href="/login">login</a>', 
                                success=True,
                                form=create_account_form)

    else:
        return render_template( 'accounts/register.html', form=create_account_form)

@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('base_blueprint.login'))

## Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('page-403.html'), 403

@blueprint.errorhandler(401)
def access_unauthorized(error):
    return render_template('page-401.html'), 401

@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('page-403.html'), 403

@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('page-404.html'), 404

@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('page-500.html'), 500

@blueprint.app_context_processor
def inject_UserTypeEnum():
    return dict(UserTypeEnum=UserTypeEnum)

@blueprint.app_context_processor
def inject_UserTypeEnumList():
    return dict(UserTypeList={i.value: i.description for i in UserTypeEnum})

@blueprint.app_context_processor
def inject_RequestStatusEnum():
    return dict(RequestStatusEnum=RequestStatusEnum)

@blueprint.app_context_processor
def inject_RequestStatusList():
    return dict(RequestStatusList={i.value: {"name": i.name, "description": i.description} for i in RequestStatusEnum})

@blueprint.app_context_processor
def inject_custom_functions():

    def status_progress_label(status: int):
        if status == 1:
            return "Draft"
        elif status > 1 and status < 6:
            return "Pending Approval"
        elif status == 6:
            return "Partially Done"
        else:
            return "Done"

    def get_percentage(min:int, max:int):
        return u"{}%".format((min / max) * 100)

    return dict(status_progress_label=status_progress_label,get_percentage=get_percentage)


@blueprint.app_template_filter()
def datetimeiso(value, format="%Y-%m-%d %H:%M:%S"):
    if not value:
        return ""
    tz = pytz.timezone('Asia/Hong_Kong')
    utc = pytz.timezone('UTC')
    value = utc.localize(value, is_dst=None).astimezone(pytz.utc)
    local_dt = value.astimezone(tz)
    return local_dt.isoformat()

@blueprint.app_template_filter()
def datetimepretty(value, format="%B %d, %Y, %I:%M %p"):
    if not value:
        return ""
    tz = pytz.timezone('Asia/Hong_Kong')
    utc = pytz.timezone('UTC')
    value = utc.localize(value, is_dst=None).astimezone(pytz.utc)
    local_dt = value.astimezone(tz)
    return local_dt.strftime(format)

@blueprint.app_template_filter()
def datepretty(value, format="%B %d, %Y"):
    if not value:
        return ""
    tz = pytz.timezone('Asia/Hong_Kong')
    utc = pytz.timezone('UTC')
    value = datetime.combine(value, datetime.min.time())
    value = utc.localize(value, is_dst=None).astimezone(pytz.utc)
    local_dt = value.astimezone(tz)
    return local_dt.strftime(format)

@blueprint.app_template_filter()
def stritdp(value, format="%B %d, %Y"):
    if not value:
        return ""
    dt = datetime.strptime(value, '%Y-%m-%d')
    return dt.strftime(format)


