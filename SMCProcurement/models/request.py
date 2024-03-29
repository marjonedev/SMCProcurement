# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_login import UserMixin, current_user
from sqlalchemy import Binary, Column, Integer, String, ForeignKey, Date, DateTime, Numeric, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum
from datetime import date, datetime
from SMCProcurement import db, login_manager
from sqlalchemy import event

from SMCProcurement.base.util import hash_pass, get_sy
from SMCProcurement.enum.request_status import RequestStatusEnum

from pprint import pprint

from SMCProcurement.enum.user_type import UserTypeEnum


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
    # approved_by_id = Column(Integer, ForeignKey("User.id"))
    # approved_by = relationship("User", backref="requests_approved", foreign_keys=[approved_by_id])
    # received_by = Column(String)
    # endorsed_by = Column(String)
    request_type_id = Column(Integer, ForeignKey("RequestType.id"))
    request_type = relationship("RequestType")
    status = Column(Integer, Enum(RequestStatusEnum), nullable=False, default=1)
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_on = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    request_lines = relationship("RequestLine", cascade="all, delete-orphan", backref="request")
    denied_remarks = Column(String)
    president_approval = Column(Boolean, default=True)

    def __init__(self, **kwargs):
        # super(Request, self).__init__(**kwargs)

        for property, value in kwargs.items():
            if hasattr(value, '__iter__') and not isinstance(value, str):
                value = value[0]
            setattr(self, property, value)

        timenow = datetime.now()
        sy = get_sy()
        self.number = "RQTEMP%s" % timenow.timestamp()
        self.sy_start = sy["start"]
        self.sy_end = sy["end"]
        self.date_requested = date.today()
        self.user_id = current_user.id
        self.department_id = current_user.department_id

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                if getattr(self, key) != value:
                    setattr(self, key, value)

    def __repr__(self):
        return str(self.number)

    @property
    def total(self):
        total: float = 0
        for item in self.request_lines:
            total += item.total

        return "%.2f" % round(float(total), 2)

    @property
    def is_confirmed(self):
        return self.status > RequestStatusEnum.draft.value

    def get_progress(self):
        min = RequestStatusEnum.draft.value
        max = RequestStatusEnum.done.value
        current = self.status

        percentage = (current / max) * 100

        if self.status == 1:
            label = "Draft"
        elif 1 < self.status < 5:
            if self.status == 4 and not self.president_approval:
                label = "Waiting for availability"
                percentage = ((current + 1) / max) * 100
            else:
                label = "Pending for Approval"
        elif self.status == 5:
            label = "Waiting for availability"
        elif self.status == 6:
            label = "Partially Done"
        else:
            label = "Done"

        status_list = {i.value: {"name": i.name, "description": i.description} for i in RequestStatusEnum}

        return {
            'min': min,
            'max': max,
            'current': current,
            'percentage': "{}%".format(percentage),
            'label': label,
            'badge': status_list[self.status]["name"]
        }

    def get_view_header(self):

        show = "none"

        if self.is_confirmed:
            if self.status == RequestStatusEnum.request.value:
                if current_user.user_type in [UserTypeEnum.vpadmin.value, UserTypeEnum.vpacad.value,
                                              UserTypeEnum.administrator.value]:
                    show = "approve"
                else:
                    show = "progress"
            elif self.status == RequestStatusEnum.vp.value:
                if current_user.user_type in [UserTypeEnum.vpfinance.value, UserTypeEnum.administrator.value]:
                    show = "approve"
                else:
                    show = "progress"
            elif self.status == RequestStatusEnum.vpfinance.value:
                if self.president_approval:
                    if current_user.user_type in [UserTypeEnum.president.value, UserTypeEnum.administrator.value]:
                        show = "approve"
                    else:
                        show = "progress"
                else:
                    show = "progress"
            else:
                show = "progress"
        else:
            if self.user_id == current_user.id:
                show = "confirm"
            elif current_user.user_type in [UserTypeEnum.administrator.value]:
                show = "confirm"
            else:
                show = "none"

        return show

    def toDataTable(self):
        d = {}

        for column in self.__table__.columns:
            value = str(getattr(self, column.name))
            d[column.name] = value

        d["department"] = self.department.name if self.department else ""
        d["user"] = self.user.full_name if self.user else ""
        statdesc = {i.value: i.description for i in RequestStatusEnum}
        statname = {i.value: i.name for i in RequestStatusEnum}
        d["status_description"] = statdesc[self.status]
        d["status_name"] = statname[self.status]

        return d


class RequestLine(db.Model, UserMixin):
    __tablename__ = 'RequestLine'

    id = Column(Integer, primary_key=True)
    request_id = Column(Integer, ForeignKey("Request.id"), nullable=False)
    item_id = Column(Integer, ForeignKey('Item.id'))
    item = relationship('Item', backref="request_lines", foreign_keys=[item_id])
    qty = Column(Integer, default=1)
    total = Column(Numeric(precision=10, scale=2), default=0.0)
    stock_in = Column(Integer, default=0)

    def __init__(self, **kwargs):

        for property, value in kwargs.items():
            if hasattr(value, '__iter__') and not isinstance(value, str):
                value = value[0]

            if property == 'qty':
                if value is None:
                    value = 0

            setattr(self, property, value)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                if getattr(self, key) != value:
                    setattr(self, key, value)

    @property
    def status(self):
        if self.request.status in [RequestStatusEnum.draft.value,
                                   RequestStatusEnum.request.value,
                                   RequestStatusEnum.vp.value,
                                   RequestStatusEnum.president.value]:
            return "Pending for Approval"
        elif self.request.status == RequestStatusEnum.vpfinance.value:
            return "Approved"
        elif self.request.status == RequestStatusEnum.denied.value:
            return "Unapproved"
        elif self.request.status == RequestStatusEnum.partial.value:
            if self.stock_in >= self.qty:
                return "Released"
            return "Partially Released"
        elif self.request.status == RequestStatusEnum.done.value:
            return "Released"
        else: return ""

    @property
    def qty_needed(self):
        qty = self.qty - self.stock_in

        if qty < 0:
            return 0

        return qty

    def toDataTable(self):
        d = {}

        for column in self.__table__.columns:
            value = str(getattr(self, column.name))
            d[column.name] = value

        return d

    def toReleaseDataTable(self):
        d = {}

        for column in self.__table__.columns:
            value = str(getattr(self, column.name))
            d[column.name] = value
        d["name"] = self.item.name
        d["category"] = self.item.category.name
        d["request"] = self.request.number
        d["department"] = self.request.department.name
        d["department_id"] = self.request.department.id
        d["price"] = self.item.unit_price
        d["qty_needed"] = self.qty_needed
        d["qty_available"] = self.item.qty

        return d


def generate_number_listener_request(mapper, connection, target):
    current_date = date.today()
    table = Request.__table__
    connection.execute(
        table.update().
            where(Request.id == target.id).
            values(number="RQ%05d" % (target.id))
    )


event.listen(Request, 'after_insert', generate_number_listener_request)
