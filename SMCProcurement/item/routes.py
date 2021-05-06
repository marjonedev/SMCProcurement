from SMCProcurement.item import blueprint
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from SMCProcurement import login_manager, db
from jinja2 import TemplateNotFound

from SMCProcurement.item.forms import ItemForm
from SMCProcurement.models import ItemCategory, Supplier
from SMCProcurement.models.item import Item

@blueprint.route('/items')
@login_required
def items():
    items = Item.query.all()
    return render_template('items/index.html', items=items)

@blueprint.route('/items/create', methods=["GET", "POST"])
@login_required
def create_item():
    form = ItemForm()
    form.category_id.choices = [(d.id, d.name) for d in ItemCategory.query.all()]
    form.supplier_id.choices = [(d.id, d.name) for d in Supplier.query.all()]

    if 'create_item' in request.form:
        item = Item(**request.form)
        db.session.add(item)
        db.session.commit()

        flash("Success! Item created.", "message")
        return redirect(url_for('item_blueprint.items'))
    else:
        return render_template('items/create.html', form=form)

@blueprint.route('/items/<id>/edit', methods=["GET", "POST"])
@login_required
def edit_item(id):
    item = db.session.query(Item).get(id)
    form = ItemForm(obj=item)
    form.category_id.choices = [(d.id, d.name) for d in ItemCategory.query.all()]
    form.supplier_id.choices = [(d.id, d.name) for d in Supplier.query.all()]

    if 'edit_item' in request.form:
        item.update(**request.form)
        db.session.commit()

        flash("Success! Item updated.", "message")
        return redirect(url_for('item_blueprint.items'))
    else:
        return render_template('items/edit.html', form=form, obj=item)

@blueprint.route('/items/<id>/delete', methods=["POST"])
@login_required
def delete_item(id):

    if 'delete_item' in request.form.to_dict():
        try:
            item = db.session.query(Item).get(id)
            db.session.delete(item)
            db.session.commit()

            flash("Success! Item deleted.", "message")
            return redirect(url_for('item_blueprint.items'))
        except Exception as msg:
            flash('Error: Unable to delete item, {}. '.format(msg), "error")
            return redirect(url_for('item_blueprint.items'))

@blueprint.route('/items/<id>', methods=["GET"])
@login_required
def view_item(id):
    try:
        item = db.session.query(Item).get(id)
        return render_template('items/view.html', obj=item)
    except:
        return render_template('page-404.html'), 404