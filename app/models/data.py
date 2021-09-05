from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class Data(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
