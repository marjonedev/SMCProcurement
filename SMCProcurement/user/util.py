# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from functools import wraps, update_wrapper

from flask import session, abort, url_for, redirect
from flask_login import current_user

from SMCProcurement import db
from SMCProcurement.models.user import User
from SMCProcurement.enum.user_type import UserTypeEnum

def is_admin():
    if "_user_id" in session:
        id = session.get("_user_id")
        user = db.session.query(User).get(id)
        return user.user_type == UserTypeEnum.administrator
    else:
        return False

def get_current_user():
    if "_user_id" in session:
        id = session.get("_user_id")
        return db.session.query(User).get(id)
    else:
        return None

# def roles_accepted(self):
#     @wraps(self)
#     def wrap(*args, **kwargs):
#         if current_user.user_type == 2:
#             return self(*args, **kwargs)
#         else:
#             abort(401)
#     return wrap

def roles_accepted(roles):
    def decorator(fn):
        def wrap(*args, **kwargs):
            print(roles)
            if current_user.user_type in roles:
                return fn(*args, **kwargs)
            else:
                abort(401)
        return update_wrapper(wrap, fn)
    return decorator