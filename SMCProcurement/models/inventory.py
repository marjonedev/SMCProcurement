# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_login import UserMixin
from sqlalchemy import Binary, Column, Integer, String, ForeignKey, Date, Numeric
from sqlalchemy.orm import relationship

from SMCProcurement import db, login_manager

class Inventory(db.Model, UserMixin):

    __tablename__ = 'Inventory'

    id = Column(Integer, primary_key=True)
    number = Column(String, nullable=False)
    request_id = Column(Integer, ForeignKey('Request.id'))
    request = relationship('Request', backref="inventories", foreign_keys=[request_id])
    user_id = Column(Integer, ForeignKey('User.id'))
    user = relationship("User", backref="inventories", foreign_keys=[user_id])
    date = Column(Date)
    inventory_items = relationship("InventoryItem", cascade="all, delete-orphan", backref="inventory")

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


class InventoryItem(db.Model, UserMixin):

    __tablename__ = 'InventoryItem'

    id = Column(Integer, primary_key=True)
    inventory_id = Column(Integer, ForeignKey('Inventory.id'), nullable=False)
    request_item_id = Column(Integer, ForeignKey('RequestLine.id'))
    item_id = Column(Integer)
    qty = Column(Integer, default=1)
    purchased_date = Column(Date)