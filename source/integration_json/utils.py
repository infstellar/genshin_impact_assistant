from source.util import *
from source.cvars import *
from pydantic import BaseModel




class PositionJson(BaseModel):
    name: str
    position: t.List
    location: str
    collection_type: str
    collection_name: str
    path: str