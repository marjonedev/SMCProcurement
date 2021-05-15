import itertools
from collections import defaultdict
from datetime import date, datetime
from pprint import pprint

import pdfkit
from sqlalchemy import func

from SMCProcurement import db
from flask import render_template, redirect, url_for, request, flash, session, abort, make_response

from SMCProcurement.enum.request_status import RequestStatusEnum
from SMCProcurement.models import Inventory, Item, InventoryItem
from SMCProcurement.pdf.pdf_manager import make_pdf_from_raw_html, make_pdf_from_url, _get_pdfkit_config
from SMCProcurement.reports import blueprint
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user
)
from SMCProcurement.reports.forms import InventoryReportForm, InventoryPrintForm
from SMCProcurement.reports.objects import InvItem


@blueprint.route('/reports/inventory', methods=["GET", "POST"])
@login_required
def inventory_reports():
    form = InventoryReportForm(request.form)

    items = []

    report_by = "1"

    if 'generate_report' in request.form:
        formData = form.data
        start_date = formData["start_date"]
        end_date = formData["end_date"]
        report_by = formData["report_by"]

        if formData["report_by"] == "1":
            items = db.session.query(Item)\
                .join(InventoryItem)\
                .join(Inventory)\
                .filter(func.DATE(Inventory.date_time) <= end_date)\
                .filter(func.DATE(Inventory.date_time) >= start_date)\
                .order_by(Inventory.date_time.asc()).all()
        else:
            items = db.session.query(Item)\
                .join(InventoryItem)\
                .join(Inventory)\
                .filter(func.DATE(Inventory.date_time) <= end_date)\
                .filter(func.DATE(Inventory.date_time) >= start_date)\
                .order_by(Item.department_id.asc(), Inventory.date_time.asc()).all()

    return render_template('reports/inventory.html', items=items, form=form, by=report_by)

@blueprint.route('/reports/inventory/print', methods=["POST"])
@login_required
def print_inventory_report():
    form = InventoryPrintForm(request.form)

    if "print_report" in request.form:
        formData = form.data
        pprint(formData["inventory_items"])
        if formData["report_by"] == "1":
            items = db.session.query(Item) \
                .join(InventoryItem) \
                .join(Inventory) \
                .filter(func.DATE(Inventory.date_time) <= formData["end_date"]) \
                .filter(func.DATE(Inventory.date_time) >= formData["start_date"]) \
                .order_by(Item.department_id.asc(), Inventory.date_time.asc()).all()
            items = __convert_to_invitems(items, formData["inventory_items"])
            html = render_template("reports/inventory_items_pdf.html", items=items, start_date=formData["start_date"], end_date=formData["end_date"])
        elif formData["report_by"] == "2":

            items = db.session.query(Item) \
                .join(InventoryItem) \
                .join(Inventory) \
                .filter(func.DATE(Inventory.date_time) <= formData["end_date"]) \
                .filter(func.DATE(Inventory.date_time) >= formData["start_date"]) \
                .order_by(Inventory.date_time.asc()).all()

            items = __convert_to_invitems(items, formData["inventory_items"])
            items = __categorize_items(items)

            html = render_template("reports/inventory_departments_pdf.html", items=items, start_date=formData["start_date"], end_date=formData["end_date"])
        else:
            html = render_template("reports/no_data_pdf.html")

        options={"enable-local-file-access": None}
        pdf = make_pdf_from_raw_html(html, options)
        response = make_response(pdf)
        response.headers["Content-Type"] = "application/pdf"
        today = date.today()
        response.headers["Content-Disposition"] = "inline; filename=inventory_report_{}.pdf".format(today)
        return response


@blueprint.route('/reports/request')
@login_required
def request_reports():
    return render_template('reports/request.html')

@blueprint.route('/reports/sample')
@login_required
def sample_report():

    return render_template("reports/inventory_items.html")

def __categorize_items(items):
    items.sort(key=lambda item: item.department)
    # for category, data in itertools.groupby(items, key=lambda item: item.department.name):
    #     print('{}: {}'.format(category, list(data)))
    return itertools.groupby(items, key=lambda item: item.department) if items else []

def __convert_to_invitems(items, inventory_items):
    invItems = []
    for item in items:
        invItems.append(InvItem(item, inventory_items))

    return list(invItems)


