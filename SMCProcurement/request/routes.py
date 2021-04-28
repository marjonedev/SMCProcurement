from SMCProcurement.enum.request_status import RequestStatusEnum
from SMCProcurement.request import blueprint
from flask import render_template, redirect, url_for, request, flash, session, abort
from flask_login import login_required, current_user
from SMCProcurement import login_manager
from jinja2 import TemplateNotFound
from SMCProcurement.models import Department, RequestLine
from SMCProcurement.models import Request
from SMCProcurement.models.request_type import RequestType
from SMCProcurement import db
from SMCProcurement.enum.user_type import UserTypeEnum
from SMCProcurement.request.forms import RequestForm
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
def all_requests():
    if current_user.user_type == UserTypeEnum.requisitor.value:
        requests = db.session.query(Request).filter(Request.user_id == current_user.id).order_by(Request.date_request)
    else:
        requests = db.session.query(Request).order_by(Request.date_request)

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


@blueprint.route('/requests/create', methods=["GET", "POST"])
@login_required
def create_request():

    if "submit_request" in request.form:

        form = RequestForm(request.form)
        form.department_id.choices = [(d.id, d.name) for d in Department.query.all()]

        formData = form.data

        data = {
            "department_id": formData["department_id"],
            "date_needed": formData["date_needed"],
            "endorsed_by": formData["endorsed_by"]
        }

        req = Request(**data)

        db.session.add(req)

        for line in formData["request_lines"]:
            lineData = {
                "name": line["name"],
                "description": line["description"],
                "qty": line["qty"],
                "unit_price": line["unit_price"]
            }
            requestLine = RequestLine(**lineData)
            req.request_lines.append(requestLine)

        db.session.commit()

        flash("Success! Request created.", "message")
        return redirect(url_for('request_blueprint.all_requests'))

    else:
        form = RequestForm()
        form.department_id.choices = [(d.id, d.name) for d in Department.query.all()]
        form.department_id.default = current_user.department_id
        form.process()
        return render_template('requests/create.html', form=form)


@blueprint.route('/requests/<id>/edit', methods=["GET", "POST"])
@login_required
def edit_request(id):

    req = db.session.query(Request).get(id)

    if req.status > RequestStatusEnum.draft.value:
        flash("Request has been confirmed. It cannot be edited!", "error")
        return redirect(url_for('request_blueprint.view_request', id=id))

    form = RequestForm(request.form, obj=req)
    form.department_id.choices = [(d.id, d.name) for d in Department.query.all()]

    if "submit_request" in request.form:
        formData = form.data
        data = {
            "department_id": formData["department_id"],
            "date_needed": formData["date_needed"],
            "endorsed_by": formData["endorsed_by"]
        }
        req.update(**data)

        searchToDeleteLine = RequestLine.query.filter(RequestLine.request_id == id).all()

        lineList = []
        for line in formData['request_lines']:
            if not line['id']:
                line.pop('id')
                reqLine = RequestLine(**line)
                req.request_lines.append(reqLine)
            else:
                lineList.append(int(line['id']))
                reqLine = db.session.query(RequestLine).get(line['id'])
                reqLine.update(**line)

        db.session.commit()

        pprint(searchToDeleteLine)
        pprint(lineList)
        for sd in searchToDeleteLine:
            if sd.id not in [i for i in lineList]:
                pprint("to delete")
                pprint(sd.id)
                db.session.query(RequestLine).filter_by(id=sd.id).delete()
                db.session.commit()


        flash("Request successfully updated!")
        return redirect(url_for('request_blueprint.view_request', id=id))

    return render_template('requests/edit.html', form=form, obj=req)


@blueprint.route('/requests/<id>/delete', methods=["POST"])
@login_required
def delete_request(id):
    if 'delete_request' in request.form.to_dict():
        try:
            req = db.session.query(Request).get(id)
            db.session.delete(req)
            db.session.commit()

            flash("Success! Request deleted.", "message")
            return redirect(url_for('request_blueprint.all_requests'))
        except Exception as msg:
            flash('Error: Unable to delete request, {}. '.format(msg), "error")
            return redirect(url_for('request_blueprint.all_requests'))

@blueprint.route('/requests/<id>/confirm', methods=["POST"])
@login_required
def confirm_request(id):
    if 'confirm_request' in request.form.to_dict():
        try:
            obj = db.session.query(Request).get(id)
            obj.status = RequestStatusEnum.request.value
            db.session.commit()
            flash("Success! Request confirmed and pending for approval.", "message")
            return redirect(url_for('request_blueprint.view_request', id=id))
        except Exception as msg:
            flash('Error: Unable to confirm the request, {}. '.format(msg), "error")
            return redirect(url_for('request_blueprint.view_request', id=id))


@blueprint.route('/requests/<id>', methods=["GET"])
@login_required
def view_request(id):

    try:
        req = db.session.query(Request).get(id)
        return render_template('requests/view.html', obj=req)
    except:
        return render_template('page-404.html'), 404