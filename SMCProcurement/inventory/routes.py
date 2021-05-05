
from SMCProcurement import db
from flask import render_template, redirect, url_for, request, flash, session, abort

from SMCProcurement.enum.request_status import RequestStatusEnum
from SMCProcurement.inventory import blueprint
from SMCProcurement.inventory.forms import InventoryForm
from SMCProcurement.models import Inventory, Request
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


@blueprint.route('/inventories/create')
@login_required
def create_inventory():
    form = InventoryForm()
    requests = db.session.query(Request).filter(Request.status > RequestStatusEnum.draft.value)\
        .filter(Request.status < RequestStatusEnum.done.value)
    form.request_id.choices = [(d.id, d.number) for d in requests]
    return render_template('inventories/create.html', form=form)

