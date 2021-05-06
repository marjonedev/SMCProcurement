from SMCProcurement.supplier import blueprint
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from SMCProcurement import login_manager, db
from jinja2 import TemplateNotFound

from SMCProcurement.supplier.forms import SupplierForm
from SMCProcurement.models.supplier import Supplier

@blueprint.route('/suppliers')
@login_required
def suppliers():
    suppliers = Supplier.query.all()
    return render_template('suppliers/index.html', suppliers=suppliers)

@blueprint.route('/suppliers/create', methods=["GET", "POST"])
@login_required
def create_supplier():
    form = SupplierForm()
    if 'create_supplier' in request.form:
        supplier = Supplier(**request.form)
        db.session.add(supplier)
        db.session.commit()

        flash("Success! Supplier created.", "message")
        return redirect(url_for('supplier_blueprint.suppliers'))
    else:
        return render_template('suppliers/create.html', form=form)

@blueprint.route('/suppliers/<id>/edit', methods=["GET", "POST"])
@login_required
def edit_supplier(id):
    supplier = db.session.query(Supplier).get(id)
    form = SupplierForm(obj=supplier)
    if 'edit_supplier' in request.form:
        supplier.update(**request.form)
        db.session.commit()

        flash("Success! Supplier updated.", "message")
        return redirect(url_for('supplier_blueprint.suppliers'))
    else:
        return render_template('suppliers/edit.html', form=form, obj=supplier)

@blueprint.route('/suppliers/<id>/delete', methods=["POST"])
@login_required
def delete_supplier(id):

    if 'delete_supplier' in request.form.to_dict():
        try:
            supplier = db.session.query(Supplier).get(id)
            db.session.delete(supplier)
            db.session.commit()

            flash("Success! Supplier deleted.", "message")
            return redirect(url_for('supplier_blueprint.suppliers'))
        except Exception as msg:
            flash('Error: Unable to delete supplier, {}. '.format(msg), "error")
            return redirect(url_for('supplier_blueprint.suppliers'))

@blueprint.route('/suppliers/<id>', methods=["GET"])
@login_required
def view_supplier(id):
    try:
        supplier = db.session.query(Supplier).get(id)
        return render_template('suppliers/view.html', obj=supplier)
    except:
        return render_template('page-404.html'), 404