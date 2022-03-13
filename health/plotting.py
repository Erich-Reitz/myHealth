import json
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class Plotting:
    @staticmethod
    def plot_weight():
        with open("body-comp.json") as body_comp:
            body_comp = json.load(body_comp)

        df = pd.DataFrame(body_comp)
        df["date"] = pd.to_datetime(df["date"])

        date = df["date"]
        weight = df["weight"]

        plt.plot(date, weight)
        plt.ylabel("Weight (Lbs)")
        plt.xlabel("Date Y/M")
        plt.show()
