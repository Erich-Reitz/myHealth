# -*- coding: utf-8 -*-

# this package
from health.health import Health
import json


if __name__ == "__main__":
    with open("user_info.json") as f:
        user_info = json.load(f)
    health = Health(user_info)
    data = health.get_body_comp_data("2019-01-01")
    with open("body_composition.json", "w") as f:
        json.dump(data, f, indent=4)

    activites = health.get_activities("cycling", "2019-01-01")
    with open("activites.json", "w") as f:
        json.dump(activites, f, indent=4)
