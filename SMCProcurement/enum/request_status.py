import enum
from . import EnumMeta


class RequestStatusEnum(enum.Enum, metaclass=EnumMeta):
    draft = 1, "Draft"
    request = 2, "Request"
    vp = 3, "VP Approved"
    vpfinance = 4, "VP Finance Approved"
    president = 5, "President Approved"
    partial = 6, "Partially Done"
    done = 7, "Done"
    denied = 8, "Unapproved"

    def __str__(self):
        return str(self.name)