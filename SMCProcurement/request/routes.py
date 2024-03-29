from SMCProcurement.enum.request_status import RequestStatusEnum
from SMCProcurement.request import blueprint
from flask import render_template, redirect, url_for, request, flash, session, abort, jsonify
from SMCProcurement import login_manager
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
        requests = db.session.query(Request) \
            .filter(Request.user_id == current_user.id) \
            .order_by(Request.date_request.desc(), Request.number.desc()).all()
    elif current_user.user_type in [UserTypeEnum.vpacad.value, UserTypeEnum.vpadmin.value]:
        requests = db.session.query(Request) \
            .join(RequestType) \
            .filter(RequestType.user_type == current_user.user_type) \
            .order_by(Request.date_request.desc(), Request.number.desc()).all()
    else:
        requests = db.session.query(Request).order_by(Request.date_request.desc(), Request.number.desc())

    return render_template('requests/index.html', requests=requests)


@blueprint.route('/requests/pending')
@login_required
def pending_requests():

    if current_user.user_type == UserTypeEnum.requisitor.value:
        requests = db.session.query(Request) \
            .filter(Request.user_id == current_user.id) \
            .filter(Request.status > RequestStatusEnum.draft.value) \
            .filter(Request.status < RequestStatusEnum.vpfinance.value) \
            .order_by(Request.date_request.desc()).all()
    elif current_user.user_type in [UserTypeEnum.vpacad.value, UserTypeEnum.vpadmin.value]:
        requests = db.session.query(Request)\
            .join(RequestType)\
            .filter(RequestType.user_type == current_user.user_type)\
            .filter(Request.status == RequestStatusEnum.request.value)\
            .order_by(Request.date_request.desc()).all()
    elif current_user.user_type == UserTypeEnum.president.value:
        requests = db.session.query(Request)\
            .filter(Request.status == RequestStatusEnum.vpfinance.value) \
            .order_by(Request.date_request.desc()).all()
    elif current_user.user_type == UserTypeEnum.vpfinance.value:
        requests = db.session.query(Request)\
            .filter(Request.status == RequestStatusEnum.vp.value) \
            .order_by(Request.date_request.desc()).all()
    else:
        requests = db.session.query(Request) \
            .filter(Request.status >= RequestStatusEnum.request.value) \
            .filter(Request.status <= RequestStatusEnum.president.value) \
            .order_by(Request.date_request.desc()).all()

    return render_template('requests/index.html', requests=requests)


@blueprint.route('/requests/create', methods=["GET", "POST"])
@login_required
def create_request():
    if "submit_request" in request.form:

        form = RequestForm(request.form)
        form.request_type_id.choices = [(d.id, d.name) for d in RequestType.query.all()]

        formData = form.data

        data = {
            "request_type_id": formData["request_type_id"],
            "date_needed": formData["date_needed"]
        }

        req = Request(**data)

        db.session.add(req)

        for line in formData["request_lines"]:
            lineData = {
                "item_id": line["item_id"],
                "qty": line["qty"],
                "total": line["total"],
            }
            requestLine = RequestLine(**lineData)
            req.request_lines.append(requestLine)

        db.session.commit()

        flash("Success! Request created.", "message")
        return redirect(url_for('request_blueprint.view_request', id=req.id))

    else:
        form = RequestForm()
        form.request_type_id.choices = [(d.id, d.name.capitalize()) for d in RequestType.query.all()]
        # form.department_id.choices = [(d.id, d.name) for d in Department.query.all()]
        # form.department_id.default = current_user.department_id
        # form.process()
        return render_template('requests/create.html', form=form)


@blueprint.route('/requests/<id>/edit', methods=["GET", "POST"])
@login_required
def edit_request(id):
    req = db.session.query(Request).get(id)

    if req.status > RequestStatusEnum.draft.value:
        flash("Request has been confirmed. It cannot be edited!", "error")
        return redirect(url_for('request_blueprint.view_request', id=id))

    form = RequestForm(request.form, obj=req)
    form.request_type_id.choices = [(d.id, d.name) for d in RequestType.query.all()]

    if "submit_request" in request.form:
        formData = form.data
        data = {
            "request_type_id": formData["request_type_id"],
            "date_needed": formData["date_needed"]
        }
        req.update(**data)

        searchToDeleteLine = RequestLine.query.filter(RequestLine.request_id == id).all()

        lineList = []
        for line in formData['request_lines']:
            if not line['id']:
                lineData = {
                    "item_id": line["item_id"],
                    "qty": line["qty"],
                    "total": line["total"],
                }
                reqLine = RequestLine(**lineData)
                req.request_lines.append(reqLine)
            else:
                lineList.append(int(line['id']))
                reqLine = db.session.query(RequestLine).get(int(line['id']))
                lineData = {
                    "qty": line["qty"],
                    "total": line["total"],
                }
                reqLine.update(**lineData)

        db.session.commit()

        for sd in searchToDeleteLine:
            if sd.id not in [i for i in lineList]:
                db.session.query(RequestLine).filter_by(id=sd.id).delete()
                db.session.commit()

        flash("Request successfully updated!")
        return redirect(url_for('request_blueprint.view_request', id=id))

    req_lines = RequestLine.query.filter(RequestLine.request_id == id).order_by(RequestLine.id.asc()).all()

    return render_template('requests/edit.html', form=form, obj=req, obj_lines=req_lines)


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
    # try:
        req = db.session.query(Request).get(id)
        req_lines = RequestLine.query.filter(RequestLine.request_id == id).order_by(RequestLine.id.asc()).all()
        return render_template('requests/view.html', obj=req, obj_lines=req_lines)
    # except:
    #     return render_template('page-404.html'), 404


@blueprint.route('/requests/<id>/approve', methods=["POST"])
@login_required
def approve_request(id):
    if 'approve_request' in request.form.to_dict():
        toPres = False
        try:
            obj = db.session.query(Request).get(id)
            approved = False

            if "president_approval" in request.form.to_dict() and obj.status == RequestStatusEnum.vp.value:
                toPres = True

            if obj.status in [RequestStatusEnum.request.value, RequestStatusEnum.vp.value,
                              RequestStatusEnum.vpfinance.value]:
                if not toPres:
                    obj.president_approval = False
                else:
                    obj.president_approval = True

                obj.status += 1
                db.session.commit()
                approved = True

            if approved:
                flash("Success! Thank you for approving this request.", "message")
                return redirect(url_for('request_blueprint.view_request', id=id))
            else:
                flash("Sadly, Nothing to approve.", "warning")
                return redirect(url_for('request_blueprint.view_request', id=id))

        except Exception as e:
            return render_template('page-404.html'), 404
    else:
        return render_template('page-404.html'), 404


@blueprint.route('/requests/<id>/decline', methods=["POST"])
@login_required
def decline_request(id):
    if 'decline_request' in request.form.to_dict():

        try:
            form = request.form.to_dict()
            if form["denied_remarks"]:
                obj = db.session.query(Request).get(id)
                obj.status = RequestStatusEnum.denied.value
                obj.denied_remarks = form["denied_remarks"]
                db.session.commit()
                flash("Request " + obj.number + " denied.", "warning")
                return redirect(url_for('request_blueprint.view_request', id=id))
            else:
                flash("Remarks field is required on decline.", "error")
                return redirect(url_for('request_blueprint.view_request', id=id))
            # obj = db.session.query(Request).get(id)
            # approved = False
            # if obj.status in [RequestStatusEnum.request.value, RequestStatusEnum.vp.value, RequestStatusEnum.president.value]:
            #     obj.status += 1
            #     db.session.commit()
            #     approved = True
            #
            # if approved:
            #     flash("Success! Thank you for approving this request.", "message")
            #     return redirect(url_for('request_blueprint.view_request', id=id))
            # else:
            #     flash("Sadly, Nothing to approve.", "warning")
            #     return redirect(url_for('request_blueprint.view_request', id=id))

        except Exception as e:
            return render_template('page-404.html'), 404
    else:
        return render_template('page-404.html'), 404


@blueprint.route('/api/requests', methods=["GET"])
@login_required
def api_get_requests():
    requests = db.session.query(Request)\
        .filter(Request.status >= RequestStatusEnum.vpfinance.value)\
        .filter(Request.status != RequestStatusEnum.denied.value)\
        .all()

    response = dict(data=[i.toDataTable() for i in requests])

    return jsonify(response)

@blueprint.route('/api/requests/items', methods=["GET"])
@login_required
def api_get_request_items():
    request_id = request.args.get('request_id')
    request_lines = db.session.query(RequestLine)\
        .filter(RequestLine.request_id == request_id)\
        .all()

    response = dict(data=[i.toDataTable() for i in request_lines])

    return jsonify(response)


