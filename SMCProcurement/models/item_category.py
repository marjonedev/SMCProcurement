# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_login import UserMixin
from sqlalchemy import Binary, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum

from SMCProcurement import db, login_manager

class ItemCategory(db.Model, UserMixin):

    __tablename__ = 'ItemCategory'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

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

    def toDict(self):
        d = {}

        for column in self.__table__.columns:
            d[column.name] = str(getattr(self, column.name))

        return d