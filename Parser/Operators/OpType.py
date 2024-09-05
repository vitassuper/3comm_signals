from enum import Enum

from Enum.EnumMeta import EnumMeta


class OpType(str, Enum, metaclass=EnumMeta):
    pass
