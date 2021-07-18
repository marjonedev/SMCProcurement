import simplejson as json
from datetime import date
from pprint import pprint

from SMCProcurement import db
from flask import render_template, redirect, url_for, request, flash, session, abort, jsonify

from SMCProcurement.enum.request_status import RequestStatusEnum
from SMCProcurement.inventory import blueprint
from SMCProcurement.inventory.forms import InventoryForm, ReleaseForm
from SMCProcurement.models import Inventory, Request, Release, Item, RequestLine
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user
)

@blueprint.route('/inventories')
@login_required
def recent_inventories():
    inv = db.session.query(Inventory).order_by(Inventory.date_time.desc(), Inventory.id.desc()).all()
    return render_template('inventories/index.html', inventories=inv)


@blueprint.route('/inventories/create', methods=["GET", "POST"])
@login_required
def create_inventory():

    if "submit" in request.form:
        form = InventoryForm(request.form)
        formData = form.data

        if not formData["inventory_items"]:
            flash("Error. Atleast one item required.", "error")
            return render_template('inventories/create.html', form=form)


        for line in formData["inventory_items"]:
            lineData = {
                "item_id": int(line["item_id"]),
                "qty": line["qty"]
            }
            inventory = Inventory(**lineData)
            db.session.add(inventory)

        db.session.commit()

        flash("Success! Inventory Created", "message")
        return redirect(url_for("inventory_blueprint.recent_inventories"))
    else:
        form = InventoryForm()
        return render_template('inventories/create.html', form=form)

@blueprint.route('/inventories/<id>', methods=["GET"])
@login_required
def view_inventory(id):
    inventory = db.session.query(Inventory).get(id)
    return render_template('inventories/view.html', obj=inventory)

@blueprint.route('/inventories/release', methods=["GET", "POST"])
@login_required
def release():

    form = ReleaseForm()

    pprint(request.form)

    if "submit" in request.form:

        try:

            form = ReleaseForm(request.form)
            formData = form.data

            if not formData["release_lines"]:
                flash("Error. Atleast one item required.", "error")
                return render_template('inventories/release.html', form=form)

            for line in formData["release_lines"]:
                lineData = {
                    "item_id": int(line["item_id"]),
                    "request_item_id": int(line["request_item_id"]),
                    "quantity": int(line["quantity"]),
                    "remarks": line["remarks"],
                    "request_id": int(line["request_id"]),
                    "department_id": int(line["department_id"])
                }
                release = Release(**lineData)
                db.session.add(release)

            db.session.commit()

            flash("Success! {} has been released.".format(release.item.name), "message")
            return redirect(url_for("inventory_blueprint.release"))

        except Exception as msg:
            flash("Error! There's a problem upon the release. {}".format(msg), "error")
            return redirect(url_for("inventory_blueprint.release"))

    return render_template('inventories/release.html', form=form)

@blueprint.route('/api/release_items', methods=["GET", "POST"])
@login_required
def get_release_items():

    exc = request.args.get("except", None)

    sesDB = db.session.query(RequestLine)

    if exc:
        exc = str(exc).split(',')
        items = sesDB.filter(RequestLine.id.notin_(exc)).all()
    else:
        items = sesDB.all()

    response = dict(data=[i.toReleaseDataTable() for i in items])

    return json.dumps(response)