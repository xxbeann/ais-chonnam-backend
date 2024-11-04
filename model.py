# 데이터를 담기위한 메모리상의 공간
from sqlalchemy import Column, String, INTEGER
from db import Base

class Menu(Base):
    __tablename__ = 'Menu'
    __table_args__ = (
        {'schema': 'public'}
    )
    food = Column(String(50), primary_key=True, nullable=False)
    rating = Column(INTEGER, nullable=False)
    courseId = Column(INTEGER, nullable=False)
