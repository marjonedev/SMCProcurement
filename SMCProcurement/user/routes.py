from SMCProcurement.user import blueprint
from flask import render_template, redirect, url_for, request, flash, session
from flask_login import login_required, current_user
from SMCProcurement import login_manager
from jinja2 import TemplateNotFound
from SMCProcurement.models.user import User
from SMCProcurement.models.department import Department
from SMCProcurement.models.request_type import RequestType
from SMCProcurement.user.forms import UserForm
from SMCProcurement import db
from SMCProcurement.enum.user_type import UserTypeEnum

from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user
)

from pprint import pprint

from SMCProcurement.user.util import roles_accepted


@blueprint.route('/users')
@login_required
@roles_accepted([UserTypeEnum.administrator])
def users():
    users = User.query.all()
    return render_template('users/index.html', users=users)

@roles_accepted([UserTypeEnum.administrator])
@blueprint.route('/users/create', methods=["GET", "POST"])
@login_required
def create_user():
    userForm = UserForm(request.form)
    userForm.department_id.choices = [(d.id, d.name) for d in Department.query.all()]
    userForm.request_type_id.choices = [(r.id, r.name) for r in RequestType.query.all()]

    if 'create_user' in request.form:

        username  = request.form['username']
        email     = request.form['email']

        # Check usename exists
        user = User.query.filter_by(username=username).first()
        if user:
            return render_template( 'users/create.html',
                                    msg='Username already registered',
                                    success=False,
                                    form=userForm)

        # Check email exists
        user = User.query.filter_by(email=email).first()
        if user:
            return render_template( 'users/create.html',
                                    msg='Email already registered',
                                    success=False,
                                    form=userForm)

        # else we can create the user
        user = User(**request.form)
        db.session.add(user)
        db.session.commit()

        flash("Success! User created.", "message")

        return redirect(url_for('user_blueprint.users'))

    else:
        return render_template('users/create.html', form=userForm)

@roles_accepted([UserTypeEnum.administrator])
@blueprint.route('/users/<id>/edit', methods=["GET", "POST"])
@login_required
def edit_user(id):
    user = db.session.query(User).get(id)
    userForm = UserForm(obj=user)
    userForm.department_id.choices = [(d.id, d.name) for d in Department.query.all()]
    userForm.request_type_id.choices = [(r.id, r.name) for r in RequestType.query.all()]

    if 'edit_user' in request.form:
        user.update(**request.form)
        db.session.commit()

        return render_template('users/edit.html', form=userForm, msg='User successfully updated.', success=False,)

    else:
        return render_template('users/edit.html', form=userForm)

@roles_accepted([UserTypeEnum.administrator])
@blueprint.route('/users/<id>/delete', methods=["POST"])
@login_required
def delete_user(id):

    if 'delete_user' in request.form.to_dict():
        try:
            uid = session.get('_user_id')
            user = db.session.query(User).get(id)
            if uid == id and user.user_type == UserTypeEnum.administrator:
                flash("Cannot delete administrator.", "error")
                return redirect(url_for('user_blueprint.users'))

            db.session.delete(user)
            db.session.commit()

            flash("Success! User deleted.", "message")
            return redirect(url_for('user_blueprint.users'))
        except Exception as msg:
            flash('Error: Unable to delete user, {}. '.format(msg), "error")
            return redirect(url_for('user_blueprint.users'))


