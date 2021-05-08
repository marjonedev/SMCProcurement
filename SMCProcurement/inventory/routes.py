from datetime import date
from pprint import pprint

from SMCProcurement import db
from flask import render_template, redirect, url_for, request, flash, session, abort

from SMCProcurement.enum.request_status import RequestStatusEnum
from SMCProcurement.inventory import blueprint
from SMCProcurement.inventory.forms import InventoryForm
from SMCProcurement.models import Inventory, Request, InventoryItem
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user
)

@blueprint.route('/inventories')
@login_required
def all_inventories():
    inv = db.session.query(Inventory).all()
    return render_template('inventories/index.html', inventories=inv)


@blueprint.route('/inventories/create', methods=["GET", "POST"])
@login_required
def create_inventory():

    if "submit" in request.form:
        form = InventoryForm(request.form)
        formData = form.data

        inventory = Inventory()
        db.session.add(inventory)

        if not formData["inventory_items"]:
            flash("Error. Atleast one item required.", "error")
            return render_template('inventories/create.html', form=form)


        for line in formData["inventory_items"]:
            if not line["purchased_date"]:
                line["purchased_date"] = date.today()
            lineData = {
                "item_id": line["item_id"],
                "purchased_date": line["purchased_date"],
                "qty": line["qty"]
            }
            invLine = InventoryItem(**lineData)
            inventory.inventory_items.append(invLine)

        db.session.commit()

        flash("Success! Inventory Created", "message")
        return redirect(url_for("inventory_blueprint.all_inventories"))
    else:
        form = InventoryForm()
        return render_template('inventories/create.html', form=form)

@blueprint.route('/inventories/<id>', methods=["GET"])
@login_required
def view_inventory(id):
    inventory = db.session.query(Inventory).get(id)
    return render_template('inventories/view.html', obj=inventory)



@blueprint.route('/inventories/reports', methods=["GET"])
@login_required
def reports():
    inv = db.session.query(Inventory).all()
    return render_template('inventories/index.html', inventories=inv)

@blueprint.route('/inventories/release', methods=["GET"])
@login_required
def release():
    inv = db.session.query(Inventory).all()
    return render_template('inventories/index.html', inventories=inv)
