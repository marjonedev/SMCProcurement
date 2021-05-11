# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from SMCProcurement.enum.request_status import RequestStatusEnum
from SMCProcurement.home import blueprint
from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user
from SMCProcurement import login_manager, db
from jinja2 import TemplateNotFound
from SMCProcurement.enum.user_type import UserTypeEnum
from SMCProcurement.models import Request


@blueprint.route('/index')
@login_required
def index():
    if current_user.user_type == UserTypeEnum.requisitor.value:
        pending = db.session.query(Request) \
            .filter(Request.user_id == current_user.id) \
            .filter(Request.status > RequestStatusEnum.draft.value) \
            .filter(Request.status < RequestStatusEnum.done.value) \
            .order_by(Request.date_request).count()
        approved = db.session.query(Request)\
            .filter(Request.user_id == current_user.id)\
            .filter(Request.status >= RequestStatusEnum.vpfinance.value)\
            .filter(Request.status < RequestStatusEnum.done.value).count()
        done = db.session.query(Request)\
            .filter(Request.user_id == current_user.id)\
            .filter(Request.status == RequestStatusEnum.done.value).count()
        total = db.session.query(Request)\
            .filter(Request.user_id == current_user.id).count()
        request_counts = {
            "pending": pending,
            "approved": approved,
            "done": done,
            "total": total,
        }
        recent = db.session.query(Request) \
            .filter(Request.user_id == current_user.id)\
            .order_by(Request.date_request).limit(10).all()
        pendinglist = db.session.query(Request) \
            .filter(Request.user_id == current_user.id) \
            .filter(Request.status > RequestStatusEnum.draft.value) \
            .filter(Request.status < RequestStatusEnum.done.value) \
            .order_by(Request.date_request).limit(10).all()
        request_lists = {
            "recent": recent,
            "pending": pendinglist
        }
        return render_template('dashboard/requisitor.html', counts=request_counts, lists=request_lists)
    elif current_user.user_type in [UserTypeEnum.vpacad.value, UserTypeEnum.vpadmin.value]:
        return render_template('dashboard/vp.html')
    elif current_user.user_type in [UserTypeEnum.president.value, UserTypeEnum.vpfinance.value]:
        return render_template('dashboard/vpfinance.html')
    elif current_user.user_type == UserTypeEnum.propertycustodian.value:
        return render_template('dashboard/custodian.html')
    else:
        return render_template('dashboard/index.html')



@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith( '.html' ):
            template += '.html'

        # Detect the current page
        segment = get_segment( request )

        # Serve the file (if exists) from app/templates/FILE.html
        return render_template( "sample/" + template, segment=segment )

    except TemplateNotFound:
        return render_template('page-404.html'), 404
    
    except:
        return render_template('page-500.html'), 500

# Helper - Extract current page name from request 
def get_segment( request ): 

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment    

    except:
        return None  
