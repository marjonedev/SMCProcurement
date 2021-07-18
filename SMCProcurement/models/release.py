# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from datetime import datetime
from pprint import pprint

from flask_login import UserMixin, current_user
from sqlalchemy import Binary, Column, Integer, String, ForeignKey, DateTime, event
from sqlalchemy.orm import relationship

from SMCProcurement import db, login_manager
from SMCProcurement.enum.request_status import RequestStatusEnum
from SMCProcurement.models import Request, Item, RequestLine


class Release(db.Model, UserMixin):
    __tablename__ = 'Release'

    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey('Item.id'))
    item = relationship('Item')
    request_item_id = Column(Integer, ForeignKey('RequestLine.id'))
    request_item = relationship('RequestLine', backref="releases", foreign_keys=[request_item_id])
    request_id = Column(Integer, ForeignKey('Request.id'))
    request = relationship('Request', backref="releases", foreign_keys=[request_id])
    user_id = Column(Integer, ForeignKey('User.id'))
    user = relationship('User', backref="releases", foreign_keys=[user_id])
    department_id = Column(Integer, ForeignKey('Department.id'))
    department = relationship('Department')
    # category_id = Column(Integer, ForeignKey('ItemCategory.id'))
    # category = relationship('ItemCategory')
    date_time = Column(DateTime, nullable=False, default=datetime.utcnow)
    quantity = Column(Integer)
    remarks = Column(String)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            if hasattr(value, '__iter__') and not isinstance(value, str):
                value = value[0]

            setattr(self, property, value)

        self.user_id = current_user.id

        request_line = db.session.query(RequestLine).get(self.request_item_id)
        item = db.session.query(Item).get(self.item_id)
        item.qty = item.qty - int(self.quantity) if item.qty else (0 - int(self.quantity))
        item.stock_out = item.stock_out + int(self.quantity) if item.stock_out else int(self.quantity)
        request_line.stock_in = request_line.stock_in + int(self.quantity) if request_line.stock_in else int(
            self.quantity)

    def __repr__(self):
        return str(self.name)

    # def update(self, **kwargs):
    #     for key, value in kwargs.items():
    #         if hasattr(self, key):
    #             if getattr(self, key) != value:
    #                 setattr(self, key, value)


def update_requisition_status_listener(mapper, connection, target):
    request = db.session.query(Request).get(target.request_id)

    qty = 0
    stockin = 0
    for i in request.request_lines:
        qty += int(i.qty) if i.qty else 0
        stockin += int(i.stock_in) if i.stock_in else 0

    if stockin >= qty:
        status = RequestStatusEnum.done.value
    else:
        status = RequestStatusEnum.partial.value

    table = Request.__table__
    connection.execute(
        table.update().
            where(Request.id == target.request_id).
            values(status=status)
    )


event.listen(Release, 'after_insert', update_requisition_status_listener)
