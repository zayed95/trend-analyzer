from sqlalchemy import Column, Integer, Text, DateTime, String
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
    keyword = Column(String, nullable=False)

    def __repr__(self):
        return f"('{self.id}', '{self.content}', '{self.keyword}', '{self.timestamp}')"

class CleanPost(Base):
    __tablename__ = "clean_post"

    id = Column(Integer, primary_key=True, index=True)
    raw_id = Column(Integer, nullable=False, unique=True)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    keyword = Column(String, nullable=False)