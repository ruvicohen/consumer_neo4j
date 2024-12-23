from typing import Optional

from dataclasses import dataclass


@dataclass
class Date:
    year: Optional[int]
    month: Optional[int]
    day: Optional[int]
