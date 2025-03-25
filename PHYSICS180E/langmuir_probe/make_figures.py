#!/usr/bin/env python3

import os
import json
import matplotlib.pyplot as plt
import numpy as np
import h5py
from scipy.optimize import curve_fit

# import analyze_IV_curves

all_data = []
for json_filename in os.listdir(".cache"):
    with open(".cache/" + json_filename) as file:
        all_data.append(json.load(file))

# Langmuir probe tip was a circle with 0.5 cm diameter
probe_area = np.pi * (2.5e-3) ** 2
# Electron mass is 0.511 MeV
m_e = 0.511e6 / 3e8 ** 2
# Electron charge (in Coulombs)
e = 1.60217663e-19
for i in range(len(all_data)):
    all_data[i]["Number density"] = all_data[i]["Electron saturation current"] / e / probe_area * np.sqrt(2 * np.pi * m_e / all_data[i]["Electron temperature"])

print(f"\n\nDone analyzing {len(all_data)} I-V curves.")
yline_data = [d for d in all_data if d["X (cm)"] == 0 and d["Trigger time (ms)"] == 1 and d["Magnetic field"] == 80]
y = [d["Y (cm)"] for d in yline_data]
temp = [d["Electron temperature"] for d in yline_data]
V_p = [d["Number density"] for d in yline_data]
plt.scatter(y, V_p)
plt.title("80G magnetic field, 1ms trigger time, X coordinate = 0")
plt.xlabel("Y coordinate (cm)")
plt.ylabel("Number density (electrons per cubic meter)")
plt.show()

def decaying_exp(x, initial_amount, decay_rate):
    return initial_amount * np.exp(-decay_rate * x)


for t in [4.5]:
    xy_data = np.zeros((11, 11))
    for i in range(11):
        for j in range(11):
            x = np.linspace(-10, 10, 11)[i]
            y = np.linspace(-10, 10, 11)[j]
            shots = [d for d in all_data if d["X (cm)"] == x and d["Y (cm)"] == y and d["Trigger time (ms)"] == t and d["Magnetic field"] == 60]
            temps = [d["Number density"] for d in shots]
            if len(temps) > 0:
                xy_data[i, j] = sum(temps) / len(temps)
            else:
                xy_data[i,j] = 0
    fig = plt.imshow(xy_data, cmap="plasma", extent=[-10, 10, -10, 10])
    plt.colorbar(fig)
    plt.xticks(np.linspace(-10, 10, 11))
    plt.yticks(np.linspace(-10, 10, 11))
    plt.xlabel("X coordinate (cm)")
    plt.ylabel("Y coordinate (cm)")
    plt.title(f"Electrons per cubic meter (B=60G, t={t}ms)")
    plt.savefig("XY_plane.png")
    plt.show()

for t in [4.5]:
    xy_data = np.zeros((11, 11))
    for i in range(11):
        for j in range(11):
            x = np.linspace(-10, 10, 11)[i]
            y = np.linspace(-10, 10, 11)[j]
            shots = [d for d in all_data if d["X (cm)"] == x and d["Y (cm)"] == y and d["Trigger time (ms)"] == t and d["Magnetic field"] == 60]
            temps = [d["Electron temperature"] for d in shots]
            if len(temps) > 0:
                xy_data[i, j] = sum(temps) / len(temps)
            else:
                xy_data[i,j] = 0
    fig = plt.imshow(xy_data, cmap="plasma", extent=[-10, 10, -10, 10])
    plt.colorbar(fig)
    plt.xticks(np.linspace(-10, 10, 11))
    plt.yticks(np.linspace(-10, 10, 11))
    plt.xlabel("X coordinate (cm)")
    plt.ylabel("Y coordinate (cm)")
    plt.title(f"Temperature in eV (B=60G, t={t}ms)")
    plt.savefig("XY_plane.png")
    plt.show()

for B in [60, 70, 80]:
    times = []
    densities = []
    temperatures = []
    for t in np.linspace(0, 4.5, 10):
        for d in all_data:
            if d["X (cm)"] != 0 or d["Y (cm)"] != 0 or d["Trigger time (ms)"] != t or d["Magnetic field"] != B:
                continue
            times.append(t)
            densities.append(d["Number density"])
            temperatures.append(d["Electron temperature"])
    plt.scatter(times, densities, label=f"{B} Gauss field", alpha=0.5)
    ### popt, cov = curve_fit(decaying_exp, densities, times, p0=[2e17, 0.5])
    ### print(popt)
    ### times = np.linspace(0, 5, 100)
    ### densities = decaying_exp(times, *popt)
    ### plt.plot(times, densities)
plt.xlabel("Time after discharge (ms)")
plt.ylabel("Electrons per cubic meter")
plt.title("Number density at center of plasma")
plt.legend()
plt.show()

def analyze_interferometer(filepath):
    with h5py.File(filepath, "r") as file:
        c3 = file["Acquisition/LeCroy_scope/Channel3"][0]
        t  = file["Acquisition/LeCroy_scope/time"][:]
        plt.plot(t, c3)
        plt.xlabel("Time after discharge (ms)")
        plt.ylabel("Interferometer measurement (V)")
        plt.title("Density during discharge and afterglow (port 4, 70G field)")
        plt.show()

path = "../../../Downloads/Langmuir probe data/Group A/"
analyze_interferometer(path + "february11/interferometer_port4_RF299V_70Guniform_1mTorr_1V_2-11-2025.hdf5")
