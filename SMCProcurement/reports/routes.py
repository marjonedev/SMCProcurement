from datetime import date
from pprint import pprint

import pdfkit
from sqlalchemy import func

from SMCProcurement import db
from flask import render_template, redirect, url_for, request, flash, session, abort, make_response

from SMCProcurement.enum.request_status import RequestStatusEnum
from SMCProcurement.models import Inventory, Item, InventoryItem
from SMCProcurement.pdf.pdf_manager import make_pdf_from_raw_html, make_pdf_from_url
from SMCProcurement.reports import blueprint
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user
)
from SMCProcurement.reports.forms import InventoryReportForm, InventoryPrintForm


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

        items = db.session.query(Item)\
            .join(InventoryItem)\
            .join(Inventory)\
            .filter(func.DATE(Inventory.date_time) <= end_date)\
            .filter(func.DATE(Inventory.date_time) >= start_date)\
            .order_by(Inventory.date_time.asc()).all()

    return render_template('reports/inventory.html', items=items, form=form, by=report_by)

@blueprint.route('/reports/inventory/print', methods=["POST"])
@login_required
def print_inventory_report():
    form = InventoryPrintForm(request.form)

    if "print_report" in request.form:
        pdf = make_pdf_from_raw_html("HELLO WORLD")
        response = make_response(pdf)
        response.headers["Content-Type"] = "application/pdf"
        response.headers["Content-Disposition"] = "inline; filename=output.pdf"
        return response


@blueprint.route('/reports/request')
@login_required
def request_reports():
    return render_template('reports/request.html')

