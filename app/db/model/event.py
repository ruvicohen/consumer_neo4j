from pydantic import BaseModel
from typing import List
from app.db.model.casualities import Casualties
from app.db.model.date import Date
from app.db.model.location import Location
from typing import Optional


class Event(BaseModel):
    fatalities: Optional[int]
    injuries: Optional[int]
    score: Optional[int]