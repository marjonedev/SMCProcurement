from SMCProcurement.user import blueprint
from flask import render_template, redirect, url_for, request, flash, session
from flask_login import login_required, current_user
from SMCProcurement import login_manager
from jinja2 import TemplateNotFound
from SMCProcurement.models.user import User
from SMCProcurement.models.department import Department
from SMCProcurement.models.request_type import RequestType
from SMCProcurement.user.forms import UserForm, UserFormIndividual
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
@roles_accepted([UserTypeEnum.administrator, UserTypeEnum.president])
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


@blueprint.route('/users/<id>/edit', methods=["GET", "POST"])
@login_required
def edit_user(id):

    user = db.session.query(User).get(id)

    if current_user.is_admin:
        userForm = UserForm(obj=user)
        userForm.request_type_id.choices = [(r.id, r.name) for r in RequestType.query.all()]
        template = 'users/edit.html'
    else:
        if current_user.id == user.id:
            userForm = UserFormIndividual(obj=user)
            template = 'users/edit_individual.html'
        else:
            return render_template('page-404.html'), 404

    userForm.department_id.choices = [(d.id, d.name) for d in Department.query.all()]

    if 'edit_user' in request.form:
        user.update(**request.form)
        db.session.commit()

        flash("User successfully updated.", "message")
        return redirect(url_for("user_blueprint.view_user", id=user.id))
    else:
        return render_template(template, form=userForm, obj=user)

@roles_accepted([UserTypeEnum.administrator])
@blueprint.route('/users/<id>/delete', methods=["POST"])
@login_required
def delete_user(id):

    if 'delete_user' in request.form.to_dict():
        try:
            user = db.session.query(User).get(id)
            if user.user_type == UserTypeEnum.administrator.value:
                flash("Cannot delete administrator.", "error")
                return redirect(url_for('user_blueprint.users'))

            db.session.delete(user)
            db.session.commit()

            flash("Success! User deleted.", "message")
            return redirect(url_for('user_blueprint.users'))
        except Exception as msg:
            flash('Error: Unable to delete user, {}. '.format(msg), "error")
            return redirect(url_for('user_blueprint.users'))


@blueprint.route('/users/<id>', methods=["GET"])
@login_required
def view_user(id):
    try:

        if current_user.user_type == UserTypeEnum.requisitor.value and current_user.id == int(id):
            allow = True
        elif current_user.user_type is not UserTypeEnum.requisitor.value:
            allow = True
        else:
            allow = False

        if allow:
            user = db.session.query(User).get(id)
            return render_template('users/view.html', obj=user)
        else:
            return render_template('page-404.html'), 404
    except:
        return render_template('page-404.html'), 404