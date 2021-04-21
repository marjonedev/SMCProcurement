import enum
from . import EnumMeta

class RequestStatusEnum(enum.Enum, metaclass=EnumMeta):
    draft = 1, "Draft"
    request = 2, "Request"
    vp = 3, "VP Approved"
    president = 4, "President Approved"
    waiting = 5, "Waiting Availability"
    available = 5, "Available"
    done = 6, "Done"

    def __str__(self):
        return str(self.value)