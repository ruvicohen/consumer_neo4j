from pydantic import BaseModel
from typing import Optional

class Location(BaseModel):
    latitude: Optional[float]
    longitude: Optional[float]
