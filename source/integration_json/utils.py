from source.util import *
from pydantic import BaseModel

LOCA_TEYVAT = 'Teyvat'
COLL_TYPE_PLANT = 'Plant'


class PositionJson(BaseModel):
    name: str
    position: t.List
    location: str
    collection_type: str
    collection_name: str
    path: str