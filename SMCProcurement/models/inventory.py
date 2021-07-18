# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from datetime import datetime, date
from pprint import pprint

from flask_login import UserMixin, current_user
from sqlalchemy import Binary, Column, Integer, String, ForeignKey, Date, Numeric, event, DateTime
from sqlalchemy.orm import relationship

from SMCProcurement import db, login_manager
from SMCProcurement.base.util import get_sy
from SMCProcurement.models.item import Item


class Inventory(db.Model, UserMixin):
    __tablename__ = 'Inventory'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('User.id'))
    user = relationship("User", backref="inventories", foreign_keys=[user_id])
    item_id = Column(Integer, ForeignKey('Item.id'))
    item = relationship('Item', backref="inventories", foreign_keys=[item_id])
    date_time = Column(DateTime, nullable=False, default=datetime.utcnow)
    sy_start = Column(Integer)
    sy_end = Column(Integer)
    qty = Column(Integer, default=0)
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_on = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            if hasattr(value, '__iter__') and not isinstance(value, str):
                value = value[0]

            setattr(self, property, value)

        sy = get_sy()
        self.sy_start = sy["start"]
        self.sy_end = sy["end"]
        self.user_id = current_user.id

        item = db.session.query(Item).get(self.item_id)
        item.qty = item.qty + self.qty if item.qty else self.qty
        item.stock_in = item.qty + self.qty if item.qty else self.qty

    def __repr__(self):
        return str(self.name)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                if getattr(self, key) != value:
                    setattr(self, key, value)