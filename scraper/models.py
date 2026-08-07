import datetime
from pydantic import BaseModel

class RawPost(BaseModel):
    content: str
    timestamp: datetime
    keyword: str

    class Config:
        arbitrary_types_allowed=True