# standard library
from dataclasses import dataclass
import datetime


@dataclass
class BodyCompData:
    """Class for hold body composition data"""

    weight: float = -1
    body_fat: float = -1
    muscle_mass: float = -1
    water_percentage: float = -1
    bmi: float = -1
    date: datetime.datetime = -1


def clean_heart_rate_data(data: list):
    return [
        item
        for item in data
        if item["heartRateValues"]
        and len(item["heartRateValues"]) > 0
        and item["restingHeartRate"] < 90
    ]


# Remove days with low heart rate data
def remove_low_heart_rate_days(data: list):
    return [
        item
        for item in data
        if item["heartRateValues"] and len(item["heartRateValues"]) > 60
    ]
