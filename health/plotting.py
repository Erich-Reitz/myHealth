"""Plotting for tool"""

import json
import math
import math
import matplotlib.pyplot as plt
import pandas as pd


class Plotting:
    def __init__(self):
        self._body_comp_data = None
        self._heart_rate_data = None

    @property
    def heart_rate_data(self):
        if self._heart_rate_data is None:
            self._heart_rate_data = self._load_heart_rate_data()
        
        return self._heart_rate_data

    @property
    def body_comp_data(self):
        if self._body_comp_data is None:
            self._body_comp_data = self._load_body_comp_data()
        
        return self._body_comp_data


    def plot(self, command):
        if command == "weight":
            self._plot_weight()

        if command == "muscle-mass":
            self._plot_muscle_mass_as_percentage()
            self._plot_pounds_of_muscle()

        if command == "body-fat":
            self._plot_body_fat()

        if command == "body-comp":
            self._plot_body_comp()
        
        if command == "heart-rate":
            self._plot_heart_rate()

    def _load_body_comp_data(self):
        with open("body-comp.json") as body_comp:
            return json.load(body_comp)
    
    def _load_heart_rate_data(self):
        with open("heart-rate.json") as heart_rate:
            return json.load(heart_rate)

    def _plot_body_comp(self):
        body_comp_df = pd.DataFrame(self.body_comp_data)
        body_comp_df["date"] = pd.to_datetime(body_comp_df["date"])

        date = body_comp_df["date"]

        body_fat = body_comp_df["body_fat"]
        weight = body_comp_df["weight"]
        # find first index of not NaN in all sequences of data
        start_indx = 0
        for index, (bf_data, w_data) in enumerate(zip(body_fat, weight)):
            if not math.isnan(bf_data) and not math.isnan(w_data):
                start_indx = index
                break

        fig, ax1 = plt.subplots()
        ax1.plot(date[start_indx:], body_fat[start_indx:], color="red")
        ax1.set_ylabel("Body Fat (%)")
        ax2 = ax1.twinx()
        ax2.plot(date[start_indx:], weight[start_indx:], color="blue")
        ax2.set_ylabel("Weight (lbs)")
        plt.xlabel("Date Y/M")
        fig.tight_layout()
        plt.show()

    def _plot_weight(self):

        body_comp_df = pd.DataFrame(self.body_comp_data)
        body_comp_df["date"] = pd.to_datetime(body_comp_df["date"])

        date = body_comp_df["date"]
        weight = body_comp_df["weight"]

        plt.plot(date, weight)
        plt.ylabel("Weight (lbs)")
        plt.xlabel("Date Y/M")
        plt.show()

    def _plot_muscle_mass_as_percentage(self):
        body_comp_df = pd.DataFrame(self.body_comp_data)
        print(body_comp_df)
        body_comp_df["date"] = pd.to_datetime(body_comp_df["date"])

        date = body_comp_df["date"]
        muscle_mass_percentage = body_comp_df["muscle_mass"]

        plt.plot(date, muscle_mass_percentage)
        plt.ylabel("Muscle Mass (%)")
        plt.xlabel("Date Y/M")
        plt.show()

    def _plot_pounds_of_muscle(self):
        body_comp_df = pd.DataFrame(self.body_comp_data)
        body_comp_df["date"] = pd.to_datetime(body_comp_df["date"])

        date = body_comp_df["date"]
        muscle_mass_percentage = body_comp_df["muscle_mass"]
        weight = body_comp_df["weight"]

        pounds_of_muscle = []
        for percntge, weight in zip(muscle_mass_percentage, weight):
            percntge /= 100
            pounds_of_muscle.append(percntge * weight)

        plt.plot(date, pounds_of_muscle)
        plt.ylabel("Muscle Mass (lbs)")
        plt.xlabel("Date Y/M")
        plt.show()

    def _plot_body_fat(self):
        body_comp_df = pd.DataFrame(self.body_comp_data)
        body_comp_df["date"] = pd.to_datetime(body_comp_df["date"])

        date = body_comp_df["date"]
        body_fat_perc = body_comp_df["body_fat"]

        plt.plot(date, body_fat_perc)
        plt.ylabel("Body Fat (%)")
        plt.xlabel("Date Y/M")
        plt.show()

    def _plot_heart_rate(self):
        heart_rate_df = pd.DataFrame(self.heart_rate_data)
        heart_rate_df["calendarDate"] = pd.to_datetime(heart_rate_df["calendarDate"])


        date = heart_rate_df["calendarDate"]
        print(date)
        hr = heart_rate_df["restingHeartRate"]
        print(hr)

        plt.plot(date, hr)
        plt.ylabel("Heart rate (bpm)")
        plt.xlabel("Date Y/M")
        plt.show()   
