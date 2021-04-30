import enum
from . import EnumMeta


class RequestStatusEnum(enum.Enum, metaclass=EnumMeta):
    draft = 1, "Draft"
    request = 2, "Request"
    vp = 3, "VP Approved"
    president = 4, "President Approved"
    vpfinance = 5, "VP Finance Approved"
    partial = 6, "Partially Done"
    done = 7, "Done"
    denied = 8, "Not Approved"

    def __str__(self):
        return str(self.name)