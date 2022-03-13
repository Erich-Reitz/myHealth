"""Plotting for tool"""

import json
import matplotlib.pyplot as plt
import pandas as pd


class Plotting:
    @staticmethod
    def plot_weight():
        with open("body-comp.json") as body_comp:
            body_comp = json.load(body_comp)

        body_comp_df = pd.DataFrame(body_comp)
        body_comp_df["date"] = pd.to_datetime(body_comp_df["date"])

        date = body_comp_df["date"]
        weight = body_comp_df["weight"]

        plt.plot(date, weight)
        plt.ylabel("Weight (Lbs)")
        plt.xlabel("Date Y/M")
        plt.show()
