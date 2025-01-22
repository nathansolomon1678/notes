#!/usr/bin/env python3

# To avoid confusion, let x represent pressure times distance, and
# do not abbreviate pandas as pd (so "pd" won't mean anything)
import pandas
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from math import log
import numpy as np

def V_b(x, c1, c2, gamma):
    return [c2 * x_val / (log(c1 * x_val) - log(log(1 + 1 / gamma))) for x_val in x]

for filename in ["argon.csv"]:
    df = pandas.read_csv(filename)
    n = len(df)
    distances = list(df["Distance (cm)"])
    pressures = list(df["Pressure (mTorr)"])
    voltages = list(df["Breakdown voltage"])
    x = [distances[i] * pressures[i] for i in range(n)]
    y = voltages
    plt.scatter(x, y)

    params, covariance = curve_fit(V_b, x, y, p0=[.000015, .27, 200], bounds=([.00001, .2, 100], [.00002, .3, 300]))
    c1, c2, gamma = params
    x = np.linspace(1, 3000, 200)
    y = V_b(x, c1, c2, gamma)
    plt.plot(x, y)

    plt.xlabel("Pressure times distance (mTorr cm)")
    plt.ylabel("Breakdown voltage (Volts)")
    plt.xlim(0, 3000)
    plt.ylim(0, 500)
    plt.show()

    print(params)
