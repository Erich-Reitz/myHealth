# standard library
import json
import datetime


# third party

# this package
from health.weight_gurus import WeightGurus
from health.garmin import Garmin


class Health:
    def __init__(self, user_info) -> None:
        self.user_info = user_info

    def pull_info(self):
        body_comp_data = self._get_body_comp_data()
        for data in body_comp_data:
            print(data)
        


    def _get_body_comp_data(self):
        wg_comp_data = self._get_weight_gurus_body_comp_data()
        garmin_comp_data = self._get_garmin_data()
        data = wg_comp_data + garmin_comp_data
        return data


    def _get_garmin_data(self):
        garmin_user_info = self.user_info['garmin']
        garmin = Garmin(garmin_user_info['username'], garmin_user_info['password'])
        garmin.login()
        data = garmin.get_body_composition("1970-01-01", datetime.date.today().isoformat())
        return data


    def _get_weight_gurus_body_comp_data(self):
        weight_gurus_info = self.user_info['weight-gurus']
        weight_gurus = WeightGurus(
            weight_gurus_info["username"], weight_gurus_info["password"]
        )
        data = weight_gurus.get_all()
        return data


def health(args):
    with open("user_info.json") as user_info:
        user_info = json.load(user_info)

    health = Health(user_info)

    if args.action == "pull":
        health.pull_info()

    return
