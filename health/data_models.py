# standard library
from dataclasses import dataclass
import datetime

# third party
from cmath import nan


@dataclass
class BodyCompData:
    """Class for hold body composition data"""

    weight: float = nan
    body_fat: float = nan
    muscle_mass: float = nan
    water_percentage: float = nan
    bmi: float = nan
    date: datetime.datetime = nan


def clean_heart_rate_data(data: list):
    new_data = []
    for item in data:
        if item["restingHeartRate"] and 30 < item["restingHeartRate"] < 90:
            new_data.append(item)

    return new_data


# Remove days with low heart rate data
def remove_low_heart_rate_days(data: list):
    new_data = []
    for item in data:
        if item["heartRateValues"]:
            # If there is more than 2 hours of heart rate data
            if len(item["heartRateValues"]) > 60:
                new_data.append(item)

    return new_data
