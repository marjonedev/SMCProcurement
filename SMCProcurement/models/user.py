# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_login import UserMixin
from sqlalchemy import Binary, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum
from SMCProcurement import db, login_manager
from SMCProcurement.base.util import hash_pass
from SMCProcurement.enum.user_type import UserTypeEnum
from pprint import pprint

class User(db.Model, UserMixin):

    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(Binary)
    first_name = Column(String)
    last_name = Column(String)
    position = Column(String)
    department_id = Column(Integer, ForeignKey('Department.id'))
    department = relationship("Department")
    user_type = Column(Integer, Enum(UserTypeEnum), nullable=False, default=100)
    request_type_id = Column(Integer, ForeignKey("RequestType.id"))
    request_type = relationship("RequestType")

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == 'password':
                value = hash_pass( value ) # we need bytes here (not plain str)
                
            setattr(self, property, value)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                if key == 'password' and not value:
                    continue
                if getattr(self, key) != value:
                    if key == 'password':
                        print("change password")
                        if not value:
                            pass
                        else:
                            value = hash_pass( value )
                    setattr(self, key, value)

    @property
    def user_type_str(self):
        arr = {i.value: i.description for i in UserTypeEnum}
        return str(arr[self.user_type])

    @property
    def full_name(self):
        fname = self.first_name if self.first_name else ""
        lname = self.last_name if self.last_name else ""
        return str("%s %s") % (fname, lname)

    def __repr__(self):
        return str(self.username)


@login_manager.user_loader
def user_loader(id):
    return User.query.filter_by(id=id).first()

@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = User.query.filter_by(username=username).first()
    return user if user else None
