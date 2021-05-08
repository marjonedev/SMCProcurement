from SMCProcurement.category import blueprint
from flask import render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user
from SMCProcurement import login_manager, db
from jinja2 import TemplateNotFound

from SMCProcurement.category.forms import CategoryForm
from SMCProcurement.models.item_category import ItemCategory

@blueprint.route('/categories')
@login_required
def categories():
    categories = ItemCategory.query.all()
    return render_template('categories/index.html', categories=categories)

@blueprint.route('/categories/create', methods=["GET", "POST"])
@login_required
def create_category():
    form = CategoryForm()
    if 'create_category' in request.form:
        category = ItemCategory(**request.form)
        db.session.add(category)
        db.session.commit()

        flash("Success! Category created.", "message")
        return redirect(url_for('category_blueprint.categories'))
    else:
        return render_template('categories/create.html', form=form)

@blueprint.route('/categories/<id>/edit', methods=["GET", "POST"])
@login_required
def edit_category(id):
    category = db.session.query(ItemCategory).get(id)
    form = CategoryForm(obj=category)
    if 'edit_category' in request.form:
        category.update(**request.form)
        db.session.commit()

        flash("Success! Category updated.", "message")
        return redirect(url_for('category_blueprint.categories'))
    else:
        return render_template('categories/edit.html', form=form, obj=category)

@blueprint.route('/categories/<id>/delete', methods=["POST"])
@login_required
def delete_category(id):

    if 'delete_category' in request.form.to_dict():
        try:
            category = db.session.query(ItemCategory).get(id)
            db.session.delete(category)
            db.session.commit()

            flash("Success! Category deleted.", "message")
            return redirect(url_for('category_blueprint.categories'))
        except Exception as msg:
            flash('Error: Unable to delete category, {}. '.format(msg), "error")
            return redirect(url_for('category_blueprint.categories'))

@blueprint.route('/api/categories', methods=["GET"])
@login_required
def api_get_categories():
    categories = db.session.query(ItemCategory).all()
    return jsonify([i.toDict() for i in categories])