#!/usr/bin/env python3

import pandas
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.signal import savgol_filter
from math import log
import numpy as np
import h5py 

path = "../../../Downloads/Langmuir probe data/Group A/february18/"
filename = "yline_RF299V_80Guniform_1mTorr_1V_tt0.5ms_R10_Tsweep750us_2-18-2025.hdf5"
with h5py.File(path + filename, "r") as file:
    shot_num = 0
    c1 = file["Acquisition/LeCroy_scope/Channel1"][shot_num][20000:80000]
    c2 = file["Acquisition/LeCroy_scope/Channel2"][shot_num][20000:80000]
    t  = list(file["Acquisition/LeCroy_scope/time"])[20000:80000]

plt.scatter(c1, c2, alpha=0.005)
c1_prime = savgol_filter(c1, 5000, 3, deriv=1)
c2_prime = savgol_filter(c2, 5000, 3, deriv=1)
c1 = savgol_filter(c1, 5000, 3)
c2 = savgol_filter(c2, 5000, 3)
slope = c2_prime / c1_prime
plt.plot([], [])
plt.plot(c1, c2)
plt.xlabel("Voltage (Volts)")
plt.ylabel("Current (Amps)")
plt.title(filename)
plt.show()

plt.plot(c1, slope)
plt.xlabel("Voltage (V)")
plt.ylabel("dI/dV")

def wgaussian(x, amplitude, mean, T):
    return amplitude * np.exp(-np.abs(x - mean) / 2 / T)
popt, cov = curve_fit(wgaussian, c1, slope, p0 = [.01, 0, 2])
best_fit = wgaussian(c1, *popt)
plt.plot(c1, best_fit)
amplitude, mean, T = popt
# Guess that area of the Langmuir probe was around (2 mm)^2
probe_area = .002 ** 2
electron_mass = (0.511e6) / (3e8 ** 2)
density = amplitude * np.sqrt(2 * np.pi * T * electron_mass) / probe_area
density /= 1.60218e-19
print(f"Electron temperature: {T} eV")
print(f"Plasma potential: {mean} V")
print(f"Electron density: {density} m^-3")

plt.show()
