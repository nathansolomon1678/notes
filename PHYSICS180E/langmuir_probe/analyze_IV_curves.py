#!/usr/bin/env python3

import pandas
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.signal import savgol_filter
from math import log
from os import listdir, mkdir
import numpy as np
import h5py
import json
import re

path = "../../../Downloads/Langmuir probe data/Group A/"
sample_rate = 1e8 # Hertz
savgol_filter_window = 5000 # Corresponds to 50 microseconds

def wgaussian(x, amplitude, mean, T):
    return amplitude * np.exp(-np.abs(x - mean) / 2 / T)

def offset_exponential(x, A, B, C):
    return np.exp(x * A) * B + C

def print_json(dictionary):
    print(json.dumps(dictionary, indent=4))

def longest_true_sequence(mask):
    # Finds the start and end index of longest continuous sequence of True values in a boolean mask
    max_len = 0
    current_len = 0
    start_index = None
    max_start_index = None
    for i, value in enumerate(mask):
        if value:
            if current_len == 0:
                start_index = i
            current_len += 1
            if current_len > max_len:
                max_len = current_len
                max_start_index = start_index
        else:
            current_len = 0
            start_index = None
    if max_start_index is None:
        return None, 0
    return max_start_index, max_start_index + max_len - 1

def relative_error(measured, expected):
    return abs((measured - expected) / expected)



def analyze_IV_curve(filepath, shot_num, plot=False):
    characteristics = {"File path": filepath}
    with h5py.File(filepath, "r") as file:
        c1 = file["Acquisition/LeCroy_scope/Channel1"][shot_num]
        positions_setup_array = list(file["Control/Positions/positions_setup_array"])
        # Isolation amplifier had a gain of 1.06
        c2 = file["Acquisition/LeCroy_scope/Channel2"][shot_num] / 1.06
        t  = list(file["Acquisition/LeCroy_scope/time"])
    
    assert len(t) in [20_000, 100_000]
    assert relative_error(len(t) / (t[len(t)-1] - t[0]), sample_rate) < 1e-4
    # Get parameters from file name
    characteristics["Magnetic field"] = int(re.compile("RF299V_([0-9]*)Guniform").search(filepath).group(1))
    characteristics["Trigger time (ms)"] = float(re.compile("_tt([0-9].[0-9])ms_").search(filepath).group(1))
    characteristics["Resistance"] = int(re.compile("_R([0-9]*)_").search(filepath).group(1))
    # Convert the voltage measurement in channel 2 to a measurement of current flowing through probe
    c2 /= characteristics["Resistance"]
    if "2-11-2025" in filepath:
        shots_per_position = 2
    else:
        shots_per_position = 5
    characteristics["Port"] = 4 if "2-18-2025" in filepath else 3
    if "yline" in filepath:
        x_coords = [0]
        y_coords = np.linspace(-10, 10, 11)
    elif "xyplane" in filepath:
        x_coords = np.linspace(-10, 10, 11)
        y_coords = np.linspace(-10, 10, 11)
    else:
        raise Exception
    assert shot_num < shots_per_position * len(x_coords) * len(y_coords)
    characteristics["X (cm)"] = float(x_coords[(shot_num // shots_per_position) % len(x_coords)])
    characteristics["Y (cm)"] = float(y_coords[shot_num // (shots_per_position * len(x_coords))])
    characteristics["Shot number"] = 1 + (shot_num % shots_per_position)
    assert characteristics["X (cm)"] == positions_setup_array[shot_num][1]
    assert characteristics["Y (cm)"] == positions_setup_array[shot_num][2]
    # Extract the sweep region
    sweep_time = 1e-6 * float(re.compile("_Tsweep([0-9]*)us_").search(filepath).group(1))
    channel_1_slope = savgol_filter(c1, savgol_filter_window, 1, deriv=1)
    mask = channel_1_slope > 0
    start, end = longest_true_sequence(mask)
    assert relative_error(t[end] - t[start], sweep_time) < .1
    c1 = c1[start:end]
    c2 = c2[start:end]
    t  =  t[start:end]
    c2_smooth = savgol_filter(c2, savgol_filter_window, 3)
    # Find floating potential -- the voltage at which no current flows
    try:
        index = np.where(c2_smooth < 0)[0][-1]
        characteristics["Floating potential"] = float(c1[index])
    except:
        characteristics["Floating potential"] = 0
    # Approximate bias voltage a perfectly affine function of time
    c1 = savgol_filter(c1, len(c1), 1)
    # Fit modified gaussian to dI/dV so that we can say everything to the left
    # of the peak of that bet fit curve is the exponential region
    dI_dV = np.gradient(c2_smooth, c1)
    p0 = [.1, c1[np.argmax(dI_dV)], 1]
    popt, cov = curve_fit(wgaussian, c1, dI_dV, p0=p0)
    best_fit = wgaussian(c1, *popt)
    amplitude, mean, T = popt
    if plot:
        plt.plot(c1, dI_dV)
        plt.plot(c1, best_fit)
        plt.show()
    # Extract the exponential region of the IV curve
    start = np.argmin(np.abs(c1 + 5))
    end = np.abs(c1 - mean).argmin()
    p0 = [.1, .001, np.mean(c2[start:end])]
    plt.plot(c1, c2)
    plt.plot(c1[start:end], offset_exponential(c1[start:end], *p0))
    plt.show()
    popt, cov = curve_fit(offset_exponential, c1[start:end], c2[start:end], p0=p0)
    best_fit = offset_exponential(c1[start:end], *popt)
    if plot:
        plt.plot(c1, c2)
        plt.plot(c1, c2_smooth)
        plt.plot(c1[:index], best_fit)
        plt.show()
    A, B, C = popt
    assert A > 0 and B > 0
    # assert C < 0
    characteristics["Ion saturation current"] = -C
    characteristics["Electron saturation current"] = float(np.max(c2_smooth))
    characteristics["Electron temperature"] = 1 / A
    # Find plasma potential -- the voltage which maximizes the current
    d2I_dV2 = savgol_filter(c2, savgol_filter_window, 4, deriv=2)
    index = np.argmin(d2I_dV2)
    characteristics["Plasma potential"] = float(c1[index])
    print_json(characteristics)
    return characteristics

if ".cache" not in listdir("."):
    mkdir(".cache")

for directory in [path + "february18/", path + "february11/"]:
    for hdf5_file_name in listdir(directory):
        if "interferometer" in hdf5_file_name:
            continue
        with h5py.File(directory + hdf5_file_name, "r") as file:
            num_shots = file["Acquisition/LeCroy_scope/Channel1"].shape[0]
        for i in range(num_shots):
            json_file_name = hdf5_file_name.split(".hdf5")[0] + f"_shot{i}.json"
            if json_file_name in listdir(".cache"):
                continue
            characteristics = analyze_IV_curve(directory + hdf5_file_name, i, True)
            with open(".cache/" + json_file_name, "w+") as file:
                json.dump(characteristics, file)
