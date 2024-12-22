from typing import Optional

from dataclasses import dataclass

@dataclass
class Casualties:
    fatalities: Optional[int]
    injuries: Optional[int]
    score: Optional[int]