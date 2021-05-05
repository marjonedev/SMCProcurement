# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from datetime import datetime, date
from flask_login import UserMixin
from sqlalchemy import Binary, Column, Integer, String, ForeignKey, Date, Numeric, event, DateTime
from sqlalchemy.orm import relationship

from SMCProcurement import db, login_manager
from SMCProcurement.base.util import get_sy


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
    sy_start = Column(Integer)
    sy_end = Column(Integer)
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_on = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            if hasattr(value, '__iter__') and not isinstance(value, str):
                value = value[0]

            setattr(self, property, value)

        timenow = datetime.now()
        self.number = "INVTEMP%s" % timenow.timestamp()
        sy = get_sy()
        self.sy_start = sy["start"]
        self.sy_end = sy["end"]
        self.date = date.today()

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


def generate_number_listener_inventory(mapper, connection, target):
    current_date = date.today()
    table = Inventory.__table__
    connection.execute(
        table.update().
            where(Inventory.id == target.id).
            values(number="INV%05d" % target.id)
    )


event.listen(Inventory, 'after_insert', generate_number_listener_inventory)
