from SMCProcurement.department import blueprint
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from SMCProcurement import login_manager, db
from jinja2 import TemplateNotFound

from SMCProcurement.department.forms import DepartmentForm
from SMCProcurement.models.department import Department

@blueprint.route('/departments')
@login_required
def departments():
    departments = Department.query.all()
    return render_template('departments/index.html', departments=departments)

@blueprint.route('/departments/create', methods=["GET", "POST"])
@login_required
def create_department():
    form = DepartmentForm()
    if 'create_department' in request.form:
        department = Department(**request.form)
        db.session.add(department)
        db.session.commit()

        flash("Success! Department created.", "message")
        return redirect(url_for('department_blueprint.departments'))
    else:
        return render_template('departments/create.html', form=form)

@blueprint.route('/departments/<id>/edit', methods=["GET", "POST"])
@login_required
def edit_department(id):
    department = db.session.query(Department).get(id)
    form = DepartmentForm(obj=department)
    if 'edit_department' in request.form:
        department.update(**request.form)
        db.session.commit()

        flash("Success! Department updated.", "message")
        return redirect(url_for('department_blueprint.departments'))
    else:
        return render_template('departments/edit.html', form=form, obj=department)

@blueprint.route('/departments/<id>/delete', methods=["POST"])
@login_required
def delete_department(id):

    if 'delete_department' in request.form.to_dict():
        try:
            department = db.session.query(Department).get(id)
            db.session.delete(department)
            db.session.commit()

            flash("Success! Department deleted.", "message")
            return redirect(url_for('department_blueprint.departments'))
        except Exception as msg:
            flash('Error: Unable to delete department, {}. '.format(msg), "error")
            return redirect(url_for('department_blueprint.departments'))