# standard library
from dataclasses import dataclass
import datetime

# third party
from numpy import NaN


@dataclass
class BodyCompData:
    """Class for hold body composition data"""

    weight: float = NaN
    body_fat: float = NaN
    muscle_mass: float = NaN
    water_percentage: float = NaN
    bmi: float = NaN
    date: datetime.datetime = NaN