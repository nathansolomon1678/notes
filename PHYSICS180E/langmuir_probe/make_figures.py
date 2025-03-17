#!/usr/bin/env python3

import os
import json
import matplotlib.pyplot as plt
import numpy as np
import h5py

# import analyze_IV_curves

all_data = []
for json_filename in os.listdir(".cache"):
    with open(".cache/" + json_filename) as file:
        all_data.append(json.load(file))

print(f"\n\nDone analyzing {len(all_data)} I-V curves.")
yline_data = [d for d in all_data if d["X (cm)"] == 0 and d["Trigger time (ms)"] == 1 and d["Magnetic field"] == 80]
print(yline_data)
y = [d["Y (cm)"] for d in yline_data]
temp = [d["Electron temperature"] for d in yline_data]
esat = [d["Electron saturation current"] for d in yline_data]
plt.scatter(y, esat)
plt.show()

# Langmuir probe tip was a circle with 0.5 cm diameter
probe_area = np.pi * (2.5e-3) ** 2
# Electron mas is 0.511 MeV
electron_mass = 0.511e6 / 3e8 ** 2
#density = amplitude * np.sqrt(2 * np.pi * T * electron_mass) / probe_area
#density /= 1.60218e-19
#print(f"Electron temperature: {T} eV")
#print(f"Plasma potential: {mean} V")
#print(f"Electron density: {density} m^-3")

def analyze_interferometer(filepath):
    with h5py.File(filepath, "r") as file:
        c3 = file["Acquisition/LeCroy_scope/Channel3"][0]
        t  = file["Acquisition/LeCroy_scope/time"][:]
        plt.plot(t, c3)
        plt.show()

path = "../../../Downloads/Langmuir probe data/Group A/"
analyze_interferometer(path + "february11/interferometer_port4_RF299V_70Guniform_1mTorr_1V_2-11-2025.hdf5")
