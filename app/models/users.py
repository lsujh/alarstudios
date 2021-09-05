from sqlalchemy import Boolean, Column, Enum, Integer, String

from app.db.base_class import Base
from app.enums.roles import Roles


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_superuser = Column(Boolean(), default=False)
    role = Column(Enum(Roles), default='manager')
