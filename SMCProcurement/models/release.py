# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_login import UserMixin
from sqlalchemy import Binary, Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship

from SMCProcurement import db, login_manager

class Release(db.Model, UserMixin):

    __tablename__ = 'Release'

    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey('Item.id'))
    item = relationship('Item')
    request_item_id = Column(Integer, ForeignKey('RequestLine.id'))
    request_item = relationship('RequestLine')
    user_id = Column(Integer, ForeignKey('User.id'))
    user = relationship('User')
    department_id = Column(Integer, ForeignKey('Department.id'))
    department = relationship('Department')
    release_date = Column(Date)
    quantity = Column(Integer)
    remarks = Column(String)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            if hasattr(value, '__iter__') and not isinstance(value, str):
                value = value[0]

            setattr(self, property, value)

    def __repr__(self):
        return str(self.name)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                if getattr(self, key) != value:
                    setattr(self, key, value)