# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import json

from flask_login import UserMixin
from sqlalchemy import Binary, Column, Integer, String, ForeignKey, Numeric, event
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum

from SMCProcurement import db, login_manager


class Item(db.Model, UserMixin):
    __tablename__ = 'Item'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    category_id = Column(Integer, ForeignKey('ItemCategory.id'), nullable=False)
    category = relationship('ItemCategory')
    department_id = Column(Integer, ForeignKey('Department.id'), nullable=False)
    department = relationship('Department')
    supplier_id = Column(Integer, ForeignKey('Supplier.id'))
    supplier = relationship('Supplier')
    item_code = Column(String)
    serial = Column(String)
    brand = Column(String)
    model = Column(String)
    description = Column(String)
    qty = Column(Integer, default=0)
    unit_price = Column(Numeric(precision=10, scale=2), default=0.0)
    stock_in = Column(Integer, default=0)
    stock_out = Column(Integer, default=0)

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

        d["category"] = {}
        if self.category:
            for col1 in self.category.__table__.columns:
                d["category"][col1.name] = str(getattr(self.category, col1.name))

        d["supplier"] = {}
        if self.supplier:
            for col2 in self.supplier.__table__.columns:
                d["supplier"][col2.name] = str(getattr(self.supplier, col2.name))

        d["department"] = {}
        if self.department:
            for col2 in self.department.__table__.columns:
                d["department"][col2.name] = str(getattr(self.department, col2.name))

        return d

    def toDataTable(self):
        d = {}

        for column in self.__table__.columns:
            value = str(getattr(self, column.name))
            d[column.name] = value

        d["category"] = self.category.name if self.category else ""
        d["supplier"] = self.supplier.name if self.supplier else ""
        d["department"] = self.department.name if self.department else ""

        return d

