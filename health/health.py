"""Main logic for tool"""

# standard library
import datetime
import logging
from typing import List
from health.data_models import BodyCompData

# third party

# this package
from health.weight_gurus import WeightGurus
from health.garmin import Garmin


# INIT LOGGER THAT PRINTS DEBUG MESSAGES
logFormat = "%(asctime)s: %(levelname)s: %(message)s"
logging.basicConfig(format=logFormat, level=logging.INFO)
LOGGER = logging.getLogger("main")
LOGGER.addHandler(logging.StreamHandler())



class Health:
    def __init__(self, user_info) -> None:
        self.garmin_username = user_info["garmin"]["username"]
        self.garmin_password = user_info["garmin"]["password"]
        self.wg_username = user_info["weight-gurus"]["username"]
        self.wg_password = user_info["weight-gurus"]["password"]

    def get_body_comp_data(self, startdate: str) -> List[BodyCompData]:
        """Return available body composition data for 'startdate' format 'YYYY-mm-dd' through enddate 'YYYY-mm-dd'."""
        wg_comp_data = self._get_weight_gurus_body_comp_data(startdate)
        garmin_comp_data = self._get_garmin_body_comp_data(startdate)
        data = wg_comp_data + garmin_comp_data
        data.sort(key=lambda body_comp: body_comp.date, reverse=False)
        return data

    def get_activities(self, activity_type: str, start_date: str, end_date=None) -> list:
        if not end_date:
            end_date = datetime.date.today().isoformat()
        garmin = Garmin(self.garmin_username, self.garmin_password)
        garmin.login()
        activities = garmin.get_activities_by_date(start_date, end_date, activity_type)

        return activities

    def _get_garmin_body_comp_data(self, startdate, enddate=None) -> List[BodyCompData]:
        garmin = Garmin(self.garmin_username, self.garmin_password)
        garmin.login()
        data = garmin.get_body_composition(startdate)
        return data

    def _get_weight_gurus_body_comp_data(self, startdate: str) -> List[BodyCompData]:
        weight_gurus = WeightGurus(self.wg_username, self.wg_password)
        data = weight_gurus.get_all(startdate)
        return data

    def get_heart_rate_data(self, startdate: str) -> list:
        data = self._get_garmin_hr_data(startdate)
        return data

    def _get_garmin_hr_data(self, startdate: str):
        # TODO: implement using startdate
        garmin = Garmin(self.garmin_username, self.garmin_password)
        garmin.login()
        data_list = []
        for i in range(0, 1300):
            date = (datetime.date.today() - datetime.timedelta(i)).isoformat()
            data = garmin.get_heart_rates(date)
            data_list.append(data)

        return data_list
