# standard library
import json

# this package
from health.health import Health
from .commonpy import json_utils


if __name__ == "__main__":
    with open("user_info.json") as f:
        user_info = json.load(f)

    health = Health(user_info)

    data = health.get_body_comp_data("2019-01-01")
    with open("pulledData/body_composition.json", "w") as f:
        json.dump(data, f, indent=4, cls=json_utils.EnhancedJSONEncoder)

    cycling = health.get_activities("cycling", "2019-01-01")
    with open("pulledData/cycling.json", "w") as f:
        json.dump(cycling, f, indent=4, cls=json_utils.EnhancedJSONEncoder)

    running = health.get_activities("running", "2019-01-01")
    with open("pulledData/running.json", "w") as f:
        json.dump(running, f, indent=4, cls=json_utils.EnhancedJSONEncoder)

    # heart_rate = health.get_heart_rate_data("2019-01-01")
    # with open("pulledData/heartrate.json" "w") as f:
    #     json.dump(heart_rate, f, indent=4, cls=json_utils.EnhancedJSONEncoder)
