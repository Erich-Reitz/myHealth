# standard library
from datetime import datetime

# third party
import requests
from numpy import NaN

# this package
from health.data_models import BodyCompData
from health.exceptions import UnknownBehavior



class WeightGurus:
    def __init__(self, username, password):
        self.login_data = {"email": username, "password": password, "web": True}
        self.headers = None
        self.start_date = "start=1970-01-01T01:00:00.504Z"
        self.weight_history = None
        self.add_weight = {}

    def __do_login(self):
        req = requests.post(
            "https://api.weightgurus.com/v3/account/login", data=self.login_data
        )
        try:
            json_data = req.json()
            self.headers = {"authorization": f"Bearer {json_data['accessToken']}"}
        except Exception as e:
            print(f"Caught Exception reading JSON: {e}")

    def __get_weight_history(self, start_date=None):
        if start_date:
            self.start_date = f"start={start_date}"
        req = requests.get(
            f"https://api.weightgurus.com/v3/operation/?{self.start_date}",
            headers=self.headers,
        )
        try:
            json_data = req.json()
        except Exception as e:
            print(f"Caught Exception reading JSON: {e}")
            json_data = None
        return json_data

    def get_all(self):
        self.__do_login()
        data = []
        operations = self.__get_weight_history()["operations"]
        operations = self._clean_operations(operations)
        for operation in operations:
            body_data: BodyCompData = self._parse_operation(operation)
            data.append(body_data)

        return data

    @staticmethod
    def _parse_operation(operation):
        weight = WeightGurus._wg_num_to_float(operation["weight"])
        body_fat = WeightGurus._wg_num_to_float(operation["bodyFat"])
        muscle_mass = WeightGurus._wg_num_to_float(operation["muscleMass"])
        water_percentage = WeightGurus._wg_num_to_float(operation["water"])
        bmi = WeightGurus._wg_num_to_float(operation["bmi"])
        date = operation["entryTimestamp"]
        return BodyCompData(weight, body_fat, muscle_mass, water_percentage, bmi, date)

    @staticmethod
    def _clean_operations(operations: list):
        operations = WeightGurus._remove_deleted_operations(operations)
        return operations

    @staticmethod
    def _remove_deleted_operations(operations):
        for index, operation in enumerate(operations):
            if operation["operationType"] == "delete":
                deleted_operation = operations.pop(index)
                operations = WeightGurus._remove_operation_deleted(
                    operations, deleted_operation
                )

        return operations

    @staticmethod
    def _remove_operation_deleted(operations, deleted_operation):
        for index, current_operation in enumerate(operations):
            if WeightGurus._is_deleted_operation(current_operation, deleted_operation):
                operations.pop(index)

        return operations

    @staticmethod
    def _is_deleted_operation(current_operation, deleted_operation):
        if (
            WeightGurus._is_operation_earlier(current_operation, deleted_operation)
            and current_operation["weight"] == deleted_operation["weight"]
        ):
            return True

        return False

    @staticmethod
    def _is_operation_earlier(current_operation, deleted_operation):
        current_date = datetime.fromisoformat(
            current_operation["serverTimestamp"].replace("Z", "+00:00")
        )
        deleted_date = datetime.fromisoformat(
            deleted_operation["serverTimestamp"].replace("Z", "+00:00")
        )
        return current_date < deleted_date

    @staticmethod
    def _wg_num_to_float(number):
        number = str(number)
        if len(number) <= 1:
            raise UnknownBehavior(
                "Unsure of how weight guru handles numbers this small"
            )

        try:
            whole_number = int(number[:-1])
        except ValueError:
            return NaN

        try:
            decimal_point = int(number[-1]) / 10
        except ValueError:
            return NaN

        return whole_number + decimal_point
