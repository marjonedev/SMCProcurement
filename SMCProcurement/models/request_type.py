# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_login import UserMixin
from sqlalchemy import Binary, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum

from SMCProcurement import db, login_manager
from SMCProcurement.enum.user_type import UserTypeEnum

from SMCProcurement.base.util import hash_pass

class RequestType(db.Model, UserMixin):

    __tablename__ = 'RequestType'

    id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String, unique=True)
    user_type = Column(Integer, Enum(UserTypeEnum))

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            setattr(self, property, value)

    def __repr__(self):
        return str(self.name)