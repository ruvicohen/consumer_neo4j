from typing import Optional
from dataclasses import dataclass

@dataclass
class Event:
    fatalities: Optional[int]
    injuries: Optional[int]
    score: Optional[int]