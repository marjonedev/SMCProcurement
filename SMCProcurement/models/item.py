# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_login import UserMixin
from sqlalchemy import Binary, Column, Integer, String, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum

from SMCProcurement import db, login_manager

class Item(db.Model, UserMixin):

    __tablename__ = 'Item'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    category_id = Column(Integer, ForeignKey('ItemCategory.id'), nullable=False)
    category = relationship('ItemCategory')
    supplier_id = Column(Integer, ForeignKey('Supplier.id'))
    supplier = relationship('Supplier')
    item_code = Column(String)
    serial = Column(String)
    brand = Column(String)
    model = Column(String)
    description = Column(String)
    qty = Column(Integer)
    unit_price = Column(Numeric(precision=10, scale=2), default=0.0)
    stock_in = Column(Integer)
    stock_out = Column(Integer)

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