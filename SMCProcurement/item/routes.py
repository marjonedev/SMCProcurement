from pprint import pprint

from SMCProcurement.item import blueprint
from flask import render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user
from SMCProcurement import login_manager, db
from jinja2 import TemplateNotFound

from SMCProcurement.item.forms import ItemForm
from SMCProcurement.models import ItemCategory, Supplier, Department, RequestLine
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

            requestLines = db.session.query(RequestLine).filter_by(item_id=id).count()
            if requestLines > 0:
                raise ValueError("Item is actively used in request")
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


@blueprint.route('/api/items', methods=["POST", "GET"])
@login_required
def get_items_json():

    exc = request.args.get("except", None)

    if exc:
        exc = str(exc).split(',')
        items = db.session.query(Item).filter(Item.id.notin_(exc)).all()
    else:
        items = db.session.query(Item).all()

    response = dict(data=[i.toDataTable() for i in items])

    return jsonify(response)


@blueprint.route('/api/items/create', methods=["POST"])
@login_required
def api_create_item():
    if 'create_item' in request.form:
        item = Item(**request.form)
        db.session.add(item)
        db.session.commit()

        return jsonify(dict(status="success", data=item.toDataTable(), message="Success! item has been created."))
    else:
        return jsonify(dict(status="error", data={}, message="Error. This event is restricted.")), 400
