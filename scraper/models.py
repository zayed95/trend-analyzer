import datetime
from pydantic import BaseModel

class RawPost(BaseModel):
    language: str
    content: str
    timestamp: datetime