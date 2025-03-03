#!/usr/bin/env python3

# To avoid confusion, let x represent pressure times distance, and
# do not abbreviate pandas as pd (so "pd" won't mean anything)
import pandas
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from math import log
import numpy as np

def V_b(x, A, B, gamma):
    return [B * x_val / (log(A * x_val) - log(log(1 + 1 / gamma))) for x_val in x]

for gas, c in [("Argon", "blue"), ("Helium", "orange"), ("Air", "green")]:
    df = pandas.read_csv(gas + ".csv")
    n = len(df)
    distances = [mesaured_distance - 2.6 for mesaured_distance in df["Distance (cm)"]]
    # pressure may be off because we forgot to calibrate barometer
    pressures = list(df["Pressure (mTorr)"])
    pd_errors = [2 * pressures[i] * .1 + distances[i] * .1 for i in range(n)]
    voltages = list(df["Breakdown voltage"])
    currents = [voltage_drop / 53400 for voltage_drop in df["Voltage across resistor"]]
    x = [distances[i] * pressures[i] for i in range(n)]
    y = voltages
    # plt.scatter(x, y)
    plt.errorbar(x, y, [2]*n, xerr=pd_errors, fmt="o", color=f"tab:{c}")

    p0 = [.01, .01, 1]
    params, covariance = curve_fit(V_b, x, y, p0=p0, bounds = ([1e-10, -np.inf, 1e-10], [np.inf, np.inf, np.inf]))
    A, B, gamma = params
    print(f"\n{gas.upper()}\n{A=}\n{B=}\n{gamma=}")
    print(f"Respective uncertainties: {np.sqrt(np.diag(covariance))}\n")
    x = np.linspace(100, 5000, 1000)
    y = V_b(x, *params)
    plt.plot(x, y, label=gas)

plt.xlabel("Pressure times distance (mTorr cm)")
plt.ylabel("Breakdown voltage (Volts)")
plt.xlim(100, 5000)
plt.ylim(200, 500)
plt.legend()
plt.savefig("curve fits.png")
plt.clf()

for gas in ["Argon", "Helium", "Air"]:
    fig = plt.figure(figsize=(8, 6))

    df = pandas.read_csv(gas + ".csv")
    n = len(df)
    distances = [mesaured_distance - 2.6 for mesaured_distance in df["Distance (cm)"]]
    # pressure may be off because we forgot to calibrate barometer
    pressures = list(df["Pressure (mTorr)"])
    voltages = list(df["Breakdown voltage"])
    currents = [voltage_drop / 53400 for voltage_drop in df["Voltage across resistor"]]
    pd = [distances[i] * pressures[i] for i in range(n)]
    plt.scatter(voltages, currents, c=pd, cmap="plasma", edgecolors="black")
    plt.title(f"Current at breakdown voltage for {gas}")
    plt.colorbar().set_label("Pressure times distance (mTorr cm)")
    plt.xlabel("Breakdown voltage (Volts)")
    plt.ylabel("Current across resistor (Amps)")
    plt.savefig(f"{gas} current at breakdown voltage.png")
    plt.clf()

df = pandas.read_csv("IV curve data.csv")
voltages = df["Battery voltage"][:-1]
currents = [v / 53400 for v in df["Resistor voltage"][:-1]]
plt.scatter(voltages, currents)
plt.xlabel("Applied voltage (Volts)")
plt.ylabel("Current across resistor (Amps)")
plt.title("IV curve for Argon at pressure of 225 mTorr, plate separation of 2.7 cm")
plt.savefig("IV curve.png")
plt.clf()
