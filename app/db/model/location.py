from typing import Optional
from dataclasses import dataclass

@dataclass
class Location:
    latitude: Optional[float]
    longitude: Optional[float]
