import enum


class EnumMeta(enum.EnumMeta):
    def __contains__(cls, item) -> bool:
        return item in cls.__members__.values()
