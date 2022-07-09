# MIT License

# Copyright (c) 2020 Ron Klinkien

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


# -*- coding: utf-8 -*-
"""Python 3 API wrapper for Garmin Connect to get your statistics."""
# standard library
import datetime
import json
import logging
import re
from typing import Any, Dict, List
import requests

# third party
import cloudscraper

# this package
from health.data_models import BodyCompData
from health.exceptions import (
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError,
    GarminConnectAuthenticationError,
)

LOGGER = logging.getLogger("main")


class ApiClient:
    """Class for a single API endpoint."""

    default_headers = {
        # 'User-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.121 Safari/535.2'
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0"
    }

    def __init__(self, session, baseurl, headers=None, aditional_headers=None):
        """Return a new Client instance."""
        self.session = session
        self.baseurl = baseurl

        if headers:
            self.headers = headers
        else:
            self.headers = self.default_headers.copy()

        if aditional_headers:
            self.headers.update(aditional_headers)

    def url(self, addurl=None):
        """Return the url for the API endpoint."""

        path = f"https://{self.baseurl}"
        if addurl is not None:
            path += f"/{addurl}"

        return path

    def get(self, addurl, aditional_headers=None, params=None):
        """Make an API call using the GET method."""
        total_headers = self.headers.copy()
        if aditional_headers:
            total_headers.update(aditional_headers)
        url = self.url(addurl)

        LOGGER.debug("URL: %s", url)
        LOGGER.debug("Headers: %s", total_headers)

        try:
            response = self.session.get(url, headers=total_headers, params=params)
            response.raise_for_status()
            # LOGGER.debug("Response: %s", response.content)
            return response
        except Exception as err:
            LOGGER.debug("Response in exception: %s", response.content)
            if response.status_code == 429:
                raise GarminConnectTooManyRequestsError("Too many requests") from err
            if response.status_code == 401:
                raise GarminConnectAuthenticationError("Authentication error") from err
            if response.status_code == 403:
                raise GarminConnectConnectionError(f"Forbidden url: {url}") from err

            raise GarminConnectConnectionError(err) from err

    def post(self, addurl, aditional_headers, params, data):
        """Make an API call using the POST method."""
        total_headers = self.headers.copy()
        if aditional_headers:
            total_headers.update(aditional_headers)
        url = self.url(addurl)

        LOGGER.debug("URL: %s", url)
        LOGGER.debug("Headers: %s", total_headers)
        LOGGER.debug("Data: %s", data)

        try:
            response = self.session.post(
                url, headers=total_headers, params=params, data=data
            )
            response.raise_for_status()
            # LOGGER.debug("Response: %s", response.content)
            return response
        except Exception as err:
            LOGGER.debug("Response in exception: %s", response.content)
            if response.status_code == 429:
                raise GarminConnectTooManyRequestsError("Too many requests") from err
            if response.status_code == 401:
                raise GarminConnectAuthenticationError("Authentication error") from err
            if response.status_code == 403:
                raise GarminConnectConnectionError(f"Forbidden url: {url}") from err

            raise GarminConnectConnectionError(err) from err


class Garmin:
    """Class for fetching data from Garmin Connect."""

    def __init__(self, email, password, is_cn=False):
        """Create a new class instance."""

        self.username = email
        self.password = password
        self.is_cn = is_cn

        self.garmin_connect_base_url = "https://connect.garmin.com"
        self.garmin_connect_sso_url = "sso.garmin.com/sso"
        self.garmin_connect_modern_url = "connect.garmin.com/modern"
        self.garmin_connect_css_url = "https://static.garmincdn.com/com.garmin.connect/ui/css/gauth-custom-v1.2-min.css"

        if self.is_cn:
            self.garmin_connect_base_url = "https://connect.garmin.cn"
            self.garmin_connect_sso_url = "sso.garmin.cn/sso"
            self.garmin_connect_modern_url = "connect.garmin.cn/modern"
            self.garmin_connect_css_url = "https://static.garmincdn.cn/cn.garmin.connect/ui/css/gauth-custom-v1.2-min.css"

        self.garmin_connect_login_url = self.garmin_connect_base_url + "/en-US/signin"
        self.garmin_connect_sso_login = "signin"

        self.garmin_connect_weight_url = "proxy/weight-service/weight/dateRange"

        self.garmin_connect_daily_sleep_url = (
            "proxy/wellness-service/wellness/dailySleepData"
        )

        self.garmin_connect_rhr = "proxy/userstats-service/wellness/daily"

        self.garmin_connect_heartrates_daily_url = (
            "proxy/wellness-service/wellness/dailyHeartRate"
        )

        self.garmin_connect_activities = (
            "proxy/activitylist-service/activities/search/activities"
        )

        self.garmin_connect_logout = "auth/logout/?url="

        self.garmin_headers = {"NK": "NT"}

        self.session = cloudscraper.CloudScraper()
        self.sso_rest_client = ApiClient(
            self.session,
            self.garmin_connect_sso_url,
            aditional_headers=self.garmin_headers,
        )
        self.modern_rest_client = ApiClient(
            self.session,
            self.garmin_connect_modern_url,
            aditional_headers=self.garmin_headers,
        )

        self.display_name = None
        self.full_name = None
        self.unit_system = None

    @staticmethod
    def __get_json(page_html, key):
        """Return json from text."""

        found = re.search(key + r" = (\{.*\});", page_html, re.M)
        if found:
            json_text = found.group(1).replace('\\"', '"')
            return json.loads(json_text)

        return None

    def login(self):
        """Login to Garmin Connect."""

        LOGGER.debug("login: %s %s", self.username, self.password)
        get_headers = {"Referer": self.garmin_connect_login_url}
        params = {
            "service": self.modern_rest_client.url(),
            "webhost": self.garmin_connect_base_url,
            "source": self.garmin_connect_login_url,
            "redirectAfterAccountLoginUrl": self.modern_rest_client.url(),
            "redirectAfterAccountCreationUrl": self.modern_rest_client.url(),
            "gauthHost": self.sso_rest_client.url(),
            "locale": "en_US",
            "id": "gauth-widget",
            "cssUrl": self.garmin_connect_css_url,
            "privacyStatementUrl": "//connect.garmin.com/en-US/privacy/",
            "clientId": "GarminConnect",
            "rememberMeShown": "true",
            "rememberMeChecked": "false",
            "createAccountShown": "true",
            "openCreateAccount": "false",
            "displayNameShown": "false",
            "consumeServiceTicket": "false",
            "initialFocus": "true",
            "embedWidget": "false",
            "generateExtraServiceTicket": "true",
            "generateTwoExtraServiceTickets": "false",
            "generateNoServiceTicket": "false",
            "globalOptInShown": "true",
            "globalOptInChecked": "false",
            "mobile": "false",
            "connectLegalTerms": "true",
            "locationPromptShown": "true",
            "showPassword": "true",
        }

        if self.is_cn:
            params[
                "cssUrl"
            ] = "https://static.garmincdn.cn/cn.garmin.connect/ui/css/gauth-custom-v1.2-min.css"

        response = self.sso_rest_client.get(
            self.garmin_connect_sso_login, get_headers, params
        )

        found = re.search(r"name=\"_csrf\" value=\"(\w*)", response.text, re.M)
        if not found:
            LOGGER.error("_csrf not found  (%d)", response.status_code)
            return False

        csrf = found.group(1)
        referer = response.url
        LOGGER.debug("_csrf found: %s", csrf)
        LOGGER.debug("Referer: %s", referer)

        data = {
            "username": self.username,
            "password": self.password,
            "embed": "false",
            "_csrf": csrf,
        }
        post_headers = {
            "Referer": referer,
            "Content-Type": "application/x-www-form-urlencoded",
        }

        response = self.sso_rest_client.post(
            self.garmin_connect_sso_login, post_headers, params, data
        )

        found = re.search(r"\?ticket=([\w-]*)", response.text, re.M)
        if not found:
            LOGGER.error("Login ticket not found (%d).", response.status_code)
            return False
        params = {"ticket": found.group(1)}

        response = self.modern_rest_client.get("", params=params)

        user_prefs = self.__get_json(response.text, "VIEWER_USERPREFERENCES")
        self.display_name = user_prefs["displayName"]
        LOGGER.debug("Display name is %s", self.display_name)

        self.unit_system = user_prefs["measurementSystem"]
        LOGGER.debug("Unit system is %s", self.unit_system)

        social_profile = self.__get_json(response.text, "VIEWER_SOCIAL_PROFILE")
        self.full_name = social_profile["fullName"]
        LOGGER.debug("Fullname is %s", self.full_name)

        return True

    def get_heart_rates(self, cdate):  #
        """Fetch available heart rates data 'cDate' format 'YYYY-mm-dd'."""

        url = f"{self.garmin_connect_heartrates_daily_url}/{self.display_name}"

        params = {"date": str(cdate)}
        LOGGER.debug("Requesting heart rates")

        data = self.modern_rest_client.get(url, params=params).json()
        return data

    def get_body_composition(self, startdate: str, enddate=None) -> List[BodyCompData]:
        """Return available body composition data for 'startdate' format 'YYYY-mm-dd' through enddate 'YYYY-mm-dd'."""
        if enddate is None:
            enddate = datetime.datetime.now().strftime("%Y-%m-%d")
        url = self.garmin_connect_weight_url
        params = {"startDate": str(startdate), "endDate": str(enddate)}

        data = self.modern_rest_client.get(url, params=params).json()
        weight_list = data["dateWeightList"]
        body_history = []
        for entry in weight_list:
            body_data: BodyCompData = self._parse_body_comp_entry(entry)
            body_history.append(body_data)

        return body_history

    @staticmethod
    def _parse_body_comp_entry(entry):
        weight = Garmin._gm_num_to_lbs_float(entry["weight"])
        date = entry["calendarDate"]
        return BodyCompData(weight=weight, date=date)

    @staticmethod
    def _gm_num_to_lbs_float(num):
        kilograms = num / 1000
        lbs = kilograms * 2.2046
        return lbs

    def get_sleep_data(self, cdate: str) -> Dict[str, Any]:
        """Return sleep data for current user."""

        url = f"{self.garmin_connect_daily_sleep_url}/{self.display_name}"
        params = {"date": str(cdate), "nonSleepBufferMinutes": 60}

        LOGGER.debug("Requesting sleep data")

        return self.modern_rest_client.get(url, params=params).json()

    def get_activities(self, start, limit):
        """Return available activities."""

        url = self.garmin_connect_activities
        params = {"start": str(start), "limit": str(limit)}
        LOGGER.debug("Requesting activities")

        return self.modern_rest_client.get(url, params=params).json()

    def get_activities_by_date(self, startdate, enddate, activitytype):
        """
        Fetch available activities between specific dates
        :param startdate: String in the format YYYY-MM-DD
        :param enddate: String in the format YYYY-MM-DD
        :param activitytype: (Optional) Type of activity you are searching
                             Possible values are [cycling, running, swimming,
                             multi_sport, fitness_equipment, hiking, walking, other]
        :return: list of JSON activities
        """

        activities = []
        start = 0
        limit = 20
        # mimicking the behavior of the web interface that fetches 20 activities at a time
        # and automatically loads more on scroll
        url = self.garmin_connect_activities
        params = {
            "startDate": str(startdate),
            "endDate": str(enddate),
            "start": str(start),
            "limit": str(limit),
        }
        if activitytype:
            params["activityType"] = str(activitytype)

        while True:
            params["start"] = str(start)
            LOGGER.debug(f"Requesting activities {start} to {start+limit}")
            act = self.modern_rest_client.get(url, params=params).json()
            if act:
                activities.extend(act)
                start = start + limit
            else:
                break

        return activities

    def logout(self):
        """Log user out of session."""

        self.modern_rest_client.get(self.garmin_connect_logout)
