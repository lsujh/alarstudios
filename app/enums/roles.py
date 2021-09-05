from enum import Enum


class ExtendedEnum(Enum):

    @classmethod
    def list(cls) -> list:
        return [item.value for item in cls]


class Roles(str, ExtendedEnum):
    admin = "Admin"
    manager = "Manager"
