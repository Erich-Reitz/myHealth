"""Main logic for tool"""

# standard library
import json
import datetime
import dataclasses

# third party

# this package
from health.weight_gurus import WeightGurus
from health.garmin import Garmin
from health.plotting import Plotting
from health.exit_codes import EXIT_SUCCESS


# pylint: disable=E0202
class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)


class Health:
    def __init__(self, user_info) -> None:
        self.user_info = user_info

    def pull(self, command):
        if command == "body-comp":
            body_comp_data = self._get_body_comp_data()
            body_comp_data.sort(key=lambda body_comp: body_comp.date, reverse=False)
            with open("body-comp.json", "w+") as json_file:
                json_file.write(json.dumps(body_comp_data, cls=EnhancedJSONEncoder))

        if command == "heart-rate":
            heart_rate_data = self._get_heart_rate_data()
            with open("heart-rate.json", "w+") as json_file:
                json_file.write(json.dumps(heart_rate_data, cls=EnhancedJSONEncoder))

        if command == "activites":
            activites = self._get_activites()
            with open("activities.json", "w+") as json_file:
                json_file.write(json.dumps(activites, cls=EnhancedJSONEncoder))

    def plot(self, command):
        plotter = Plotting()
        plotter.plot(command)

    def _get_body_comp_data(self) -> list:
        wg_comp_data = self._get_weight_gurus_body_comp_data()
        garmin_comp_data = self._get_garmin_body_comp_data()
        data = wg_comp_data + garmin_comp_data
        return data

    def _get_garmin_body_comp_data(self):
        garmin_user_info = self.user_info["garmin"]
        garmin = Garmin(garmin_user_info["username"], garmin_user_info["password"])
        garmin.login()
        data = garmin.get_body_composition(
            "1970-01-01", datetime.date.today().isoformat()
        )
        return data

    def _get_weight_gurus_body_comp_data(self):
        weight_gurus_info = self.user_info["weight-gurus"]
        weight_gurus = WeightGurus(
            weight_gurus_info["username"], weight_gurus_info["password"]
        )
        data = weight_gurus.get_all()
        return data

    def _get_heart_rate_data(self):
        data = self._get_garmin_hr_data()
        return data

    def _get_garmin_hr_data(self):
        garmin_user_info = self.user_info["garmin"]
        garmin = Garmin(garmin_user_info["username"], garmin_user_info["password"])
        garmin.login()
        data_list = []
        for i in range(0, 1300):
            date = (datetime.date.today() - datetime.timedelta(i)).isoformat()
            print(date)
            data = garmin.get_heart_rates(date)
            data_list.append(data)

        return data_list

    def _get_activites(self):
        garmin_user_info = self.user_info["garmin"]
        garmin = Garmin(garmin_user_info["username"], garmin_user_info["password"])
        garmin.login()
        start = (datetime.date.today() - datetime.timedelta(1000)).isoformat()
        activities = garmin.get_activities_by_date(
            start, datetime.date.today(), "running"
        )

        return activities


def health(args):
    with open("user_info.json") as user_info:
        user_info = json.load(user_info)

    health = Health(user_info)

    if args.pull:
        health.pull(args.pull)

    if args.plot:
        health.plot(args.plot)

    return EXIT_SUCCESS
