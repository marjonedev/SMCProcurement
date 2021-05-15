import itertools
from collections import defaultdict
from datetime import date, datetime
from pprint import pprint

import pdfkit
from sqlalchemy import func

from SMCProcurement import db
from flask import render_template, redirect, url_for, request, flash, session, abort, make_response

from SMCProcurement.enum.request_status import RequestStatusEnum
from SMCProcurement.models import Inventory, Item, InventoryItem, RequestLine, Request
from SMCProcurement.pdf.pdf_manager import make_pdf_from_raw_html, make_pdf_from_url, _get_pdfkit_config
from SMCProcurement.reports import blueprint
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user
)
from SMCProcurement.reports.forms import InventoryReportForm, InventoryPrintForm, RequestReportForm, RequestPrintForm
from SMCProcurement.reports.objects import InvItem, RQItem


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

        if formData["report_by"] == "1":
            items = db.session.query(Item) \
                .join(InventoryItem) \
                .join(Inventory) \
                .filter(func.DATE(Inventory.date_time) <= formData["end_date"]) \
                .filter(func.DATE(Inventory.date_time) >= formData["start_date"]) \
                .order_by(Inventory.date_time.asc()).all()
            items = __convert_to_invitems(items, formData["inventory_items"])
            html = render_template("reports/inventory_items_pdf.html", items=items, start_date=formData["start_date"], end_date=formData["end_date"])
        elif formData["report_by"] == "2":
            items = db.session.query(Item) \
                .join(InventoryItem) \
                .join(Inventory) \
                .filter(func.DATE(Inventory.date_time) <= formData["end_date"]) \
                .filter(func.DATE(Inventory.date_time) >= formData["start_date"]) \
                .order_by(Item.department_id.asc(), Inventory.date_time.asc()).all()

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

def __convert_to_invitems(items, inventory_items):
    invItems = []
    for item in items:
        invItems.append(InvItem(item, inventory_items))

    return list(invItems)

@blueprint.route('/reports/request', methods=["GET", "POST"])
@login_required
def request_reports():

    form = RequestReportForm(request.form)

    items = []

    report_by = "1"

    if 'generate_report' in request.form:
        formData = form.data
        start_date = formData["start_date"]
        end_date = formData["end_date"]
        report_by = formData["report_by"]

        if formData["report_by"] == "1":
            items = db.session.query(RequestLine)\
                .join(Request)\
                .filter(Request.status > RequestStatusEnum.draft.value)\
                .filter(func.DATE(Request.date_request) <= end_date)\
                .filter(func.DATE(Request.date_request) >= start_date)\
                .order_by(Request.date_request.asc(), Request.number.asc()).all()
        else:
            items = db.session.query(RequestLine)\
                .join(Request)\
                .filter(Request.status > RequestStatusEnum.draft.value)\
                .filter(func.DATE(Request.date_request) <= end_date)\
                .filter(func.DATE(Request.date_request) >= start_date)\
                .order_by(Request.department_id.asc(), Request.date_request.asc(), Request.number.asc()).all()

    return render_template('reports/request.html', items=items, form=form, by=report_by)

@blueprint.route('/reports/request/print', methods=["POST"])
@login_required
def print_request_report():
    form = RequestPrintForm(request.form)

    if "print_report" in request.form:
        formData = form.data
        if formData["report_by"] == "1":
            items = db.session.query(RequestLine) \
                .join(Request) \
                .filter(Request.status > RequestStatusEnum.draft.value) \
                .filter(func.DATE(Request.date_request) <= formData["end_date"]) \
                .filter(func.DATE(Request.date_request) >= formData["start_date"]) \
                .order_by(Request.date_request.asc(), Request.number.asc()).all()

            items = __convert_to_rqitems(items, formData["request_items"])
            html = render_template("reports/request_items_pdf.html", items=items, start_date=formData["start_date"], end_date=formData["end_date"])

        elif formData["report_by"] == "2":

            items = db.session.query(RequestLine) \
                .join(Request) \
                .filter(Request.status > RequestStatusEnum.draft.value) \
                .filter(func.DATE(Request.date_request) <= formData["end_date"]) \
                .filter(func.DATE(Request.date_request) >= formData["start_date"]) \
                .order_by(Request.department_id.asc(), Request.date_request.asc(), Request.number.asc()).all()

            items = __convert_to_rqitems(items, formData["request_items"])
            items = __categorize_items(items)

            # for category, data in items:
            #     print('{}: {}'.format(category, [i.name for i in data]))

            html = render_template("reports/request_departments_pdf.html", items=items, start_date=formData["start_date"], end_date=formData["end_date"])
        else:
            html = render_template("reports/no_data_pdf.html")

        options={"enable-local-file-access": None}
        pdf = make_pdf_from_raw_html(html, options)
        response = make_response(pdf)
        response.headers["Content-Type"] = "application/pdf"
        today = date.today()
        response.headers["Content-Disposition"] = "inline; filename=requisition_report_{}.pdf".format(today)
        return response

def __convert_to_rqitems(items, request_items):
    rqItems = []
    for item in items:
        rqItems.append(RQItem(item, request_items))

    return list(rqItems)

def __categorize_items(items):

    items.sort(key=lambda item: item.department)
    # for category, data in itertools.groupby(items, key=lambda item: item.department):
    #     print('{}: {}'.format(category, list(data)))
    return itertools.groupby(items, key=lambda item: item.department) if items else []

