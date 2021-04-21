# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_login import UserMixin
from sqlalchemy import Binary, Column, Integer, String, ForeignKey, Date, DateTime, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum
from datetime import date, datetime
from SMCProcurement import db, login_manager
from sqlalchemy import event

from SMCProcurement.base.util import hash_pass
from SMCProcurement.enum.request_status import RequestStatusEnum

from pprint import pprint

class Request(db.Model, UserMixin):

    __tablename__ = 'Request'

    id = Column(Integer, primary_key=True)
    number = Column(String, nullable=False, unique=True)
    user_id = Column(Integer, ForeignKey("User.id"), nullable=False)
    user = relationship("User", backref="requests", foreign_keys=[user_id])
    department_id = Column(Integer, ForeignKey("Department.id"))
    department = relationship("Department")
    sy_start = Column(Integer)
    sy_end = Column(Integer)
    date_request = Column(Date, default=date.today())
    date_needed = Column(Date)
    approved_by = Column(Integer, ForeignKey("User.id"))
    received_by = Column(String)
    endorsed_by = Column(String)
    request_type_id = Column(Integer, ForeignKey("RequestType.id"))
    request_type = relationship("RequestType")
    status = Column(Integer, Enum(RequestStatusEnum), nullable=False, default=1)
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_on = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    request_lines = relationship("RequestLine", cascade="all, delete-orphan", backref="request")

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            setattr(self, property, value)

        timenow = datetime.now()
        self.number = "RQTEMP%s" % timenow.timestamp()


    def __repr__(self):
        return str(self.number)


class RequestLine(db.Model, UserMixin):

    __tablename__ = 'RequestLine'

    id = Column(Integer, primary_key=True)
    request_id = Column(Integer, ForeignKey("Request.id"), nullable=False)
    description = Column(String)
    qty = Column(Integer, default=1)
    unit_price = Column(Numeric(precision=10, scale=2), default=0.0)
    total = Column(Numeric(precision=10, scale=2), default=0.0)

    def __init__(self, **kwargs):

        for property, value in kwargs.items():
            if hasattr(value, '__iter__') and not isinstance(value, str):
                value = value[0]

            setattr(self, property, value)

        self.total = self.qty * self.unit_price


def generate_number_listener(mapper, connection, target):
    current_date = date.today()
    table = Request.__table__
    connection.execute(
        table.update().
            where(Request.id == target.id).
            values(number="RQ%s%05d" % (str(current_date.year), target.id))
    )

event.listen(Request, 'after_insert', generate_number_listener)
