import enum


class StrEnumMeta(enum.EnumMeta):
    def __contains__(cls, item: str) -> bool:
        return item in cls.__members__.values()
