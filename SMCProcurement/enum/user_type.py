import enum
from . import EnumMeta

class UserTypeEnum(enum.Enum, metaclass=EnumMeta):
    administrator = 1, "Administrator"
    president = 10, "President"
    vpadmin = 11, "VP Administrator"
    vpacad = 12, "VP Academics"
    vpfinance = 13, "VP Finance"
    requisitor = 100, "Requisitor"

    def __str__(self):
        return str(self.name)