from sqlalchemy import Column, Integer, Text, DateTime, Enum as SQLEnum
from sqlalchemy.orm import declarative_base
from enum import Enum

Base = declarative_base()

class Language(str, Enum):
    ENGLISH = "en"

class RawPost(Base):
    __tablename__ = "raw_post"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    language = Column(SQLEnum(Language), nullable=False)
