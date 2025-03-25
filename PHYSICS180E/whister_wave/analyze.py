#!/usr/bin/env python3

import matplotlib.pyplot as plt
from scipy.optimize import curve_fit, minimize
from os import listdir
import numpy as np
import h5py

path = "../../../Downloads/group A mar 6 whistler wave data/"
zline_files   = [path + file for file in listdir(path) if "zline"   in file]
xzplane_files = [path + file for file in listdir(path) if "xzplane" in file]
zline_files.sort(key = lambda name: int(name.split("zline_")[1].split("MHz")[0]))

experimental_k = {
    40: 0.7,
    50: 0.8,
    60: 0.9,
    70: 0.9,
    80: 1.1,
    90: 1.2,
    100: 1.3,
    110: 1.4,
    120: 1.5,
}
experimental_k_err = dict()
# Time at which the first reflected wave appears
experimental_reflection_start = {
    40: 2.7e-7,
    50: 2.2e-7,
    60: 2.1e-7,
    70: 2e-7,
    80: 2.1e-7,
    90: 1.85e-7,
    100: 1.85e-7,
    110: 1.8e-7,
    120: 1.8e-7,
}

def exponential(x, A, r):
    return np.multiply(A, np.exp(np.multiply(r, x)))

def cosine(x, A, k, phase):
    return np.multiply(A, np.cos(np.multiply(k, x) + phase))

def complex_exp_damped(x, amplitude, k, damping_coeff):
    # Treat damping_coeff as if it's negative, because wave propagates in -z direction
    return amplitude * np.exp(np.multiply(x, 1j * k + damping_coeff))

for filename in zline_files:
    freq = 1e6 * int(filename.split("zline_")[1].split("MHz")[0])
    omega = freq * 2 * np.pi
    with h5py.File(filename, "r") as file:
        t = list(file["Acquisition/LeCroy_scope/time"])
        t -= t[0]
        positions_setup_array = list(file["Control/Positions/positions_setup_array"])
        z     = [bleh[1] for bleh in positions_setup_array]
        theta = [bleh[2] for bleh in positions_setup_array]
        dt = t[-1] / (len(t) - 1)
        dz = (z[-1] - z[0]) / (len(z) - 1)
        # Voltage measured in each channel (before being amplified x10000)
        V_x = np.matrix(file["Acquisition/LeCroy_scope/Channel1"]) / 10000
        V_y = np.matrix(file["Acquisition/LeCroy_scope/Channel2"]) / 10000
        V_z = np.matrix(file["Acquisition/LeCroy_scope/Channel4"]) / 10000
        # Use Faraday's law to get magnetic flux through each wire loop
        loop_area = np.pi * (0.013 ** 2)
        B_x = (0 - np.cumsum(V_x, axis=1)) * dt / loop_area
        B_y = (0 - np.cumsum(V_y, axis=1)) * dt / loop_area
        B_z = (0 - np.cumsum(V_z, axis=1)) * dt / loop_area
        # Convert Tesla to Gauss
        B_x *= 1e4
        B_y *= 1e4
        B_z *= 1e4
    fig = plt.imshow(B_x, cmap="plasma", extent=[t[0], t[-1], z[-1], z[0]], aspect="auto")
    plt.colorbar(fig)
    plt.xticks(t[::125])
    plt.yticks(z[::6])
    plt.xlabel("Time (seconds)")
    plt.ylabel("Z coordinate (cm)")
    plt.title(f"$B_x(z, t)$ in Gauss, where f={int(freq / 1e6)}MHz")
    plt.show()
    # Integrating over time causes noise to accumulate, so use (dB / dt) instead
    dBx_dt = np.gradient(B_x, axis=1) / dt
    dBy_dt = np.gradient(B_y, axis=1) / dt
    dBz_dt = np.gradient(B_z, axis=1) / dt
    dBx_dt -= np.mean(dBx_dt)
    dBy_dt -= np.mean(dBy_dt)
    dBz_dt -= np.mean(dBz_dt)
    # Make HSV plot. This code is taken from
    # https://stackoverflow.com/questions/56577154/matplotlib-heatmap-of-complex-numbes-modulus-and-phase-as-hue-and-value
    T, Z = np.meshgrid(t, z)
    dB_dt = dBx_dt + 1j * dBy_dt
    black = np.full((*dB_dt.shape, 4), 0.)
    black[:,:,-1] = np.abs(dB_dt) / np.abs(dB_dt).max()
    black[:,:,-1] = 1 - black[:,:,-1]
    fig, ax = plt.subplots()
    ax.imshow(np.angle(dB_dt), cmap="hsv", extent=[t[0], t[-1], z[-1], z[0]], aspect="auto")
    ax.imshow(black, extent=[t[0], t[-1], z[-1], z[0]], aspect="auto")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Z coordinate (cm)")
    plt.title(f"$(\\dot{{B_x}}(z, t) + i \\dot{{B_y}}(z,t))$\n(where f={int(freq / 1e6)}MHz=$\\omega/2\\pi$)")
    plt.show()

    freq = int(freq / 1e6)
    # Multiply by exp(-i*omega*t) to remove time dependence from dB_dt
    dB_dt = np.multiply(dB_dt, np.exp(-1j * omega * T))
    # Crop off everything that appears to be a reflected wave
    mask = T <= experimental_reflection_start[freq] - experimental_k[freq] / omega * Z
    dB_dt = np.where(mask, dB_dt, 0)
    # Plot again
    black = np.full((*dB_dt.shape, 4), 0.)
    black[:,:,-1] = np.abs(dB_dt) / np.abs(dB_dt).max()
    black[:,:,-1] = 1 - black[:,:,-1]
    fig, ax = plt.subplots()
    ax.imshow(np.angle(dB_dt), cmap="hsv", extent=[t[0], t[-1], z[-1], z[0]], aspect="auto")
    ax.imshow(black, extent=[t[0], t[-1], z[-1], z[0]], aspect="auto")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Z coordinate (cm)")
    plt.title(f"$(\\dot{{B_x}}(z, t) + i \\dot{{B_y}}(z,t)) \\exp(-i \\omega t)$\n(where f={freq}MHz=$\\omega/2\\pi$)")
    plt.show()
    wave_re = np.real(np.mean(dB_dt, axis=1)).T.tolist()
    wave_im = np.imag(np.mean(dB_dt, axis=1)).T.tolist()
    wave = wave_re + np.multiply(1j, wave_im)
    # Make initial phase zero
    wave *= np.abs(wave[0]) / wave[0]
    wave_re = np.real(wave)
    wave_im = np.imag(wave)

    plt.plot(z, wave_re, label="Real component")
    plt.plot(z, wave_im, label="Imaginary component")
    plt.xlabel("Z coordinate (cm)")
    plt.ylabel(f"$\\dot{{B}}(z)$, in Gauss per second")
    plt.title(f"f={freq}MHz")
    print(f"\nFrequency: {freq} MHz")
    # Fit real component to cosine function, to find frequency
    p0 = [np.sqrt(2 * np.mean(wave_re ** 2)), experimental_k[freq], 0]
    popt, cov = curve_fit(cosine, z - z[0], wave_re, p0=p0)
    amplitude, k, phase = popt
    best_fit_cos = cosine(z - z[0], *popt) / amplitude
    k_err = 2 * np.sqrt(cov[1, 1])
    print(f"k = ({k:.7f} +/- {k_err:.7f}) cm^-1")
    # Convert cm^-1 to m^-1
    experimental_k[freq] = k * 100
    experimental_k_err[freq] = 2 * k_err * 100
    # Fit magnitude to exponential, to find decay rate
    wave_mag = np.abs(wave)
    p0 = [wave_mag[0], 0.1]
    popt, cov = curve_fit(exponential, z, wave_mag, p0=p0)
    amplitude, damping_coeff = popt
    Q_factor = np.sqrt(damping_coeff**2 + k**2) / (2 * damping_coeff)
    lambda_err = 2 * np.sqrt(cov[1, 1])
    best_fit_exp = exponential(z, *popt)
    best_fit = best_fit_cos * best_fit_exp
    plt.plot(z, best_fit, label=f"Complex exponential best fit")
    print(f"damping coefficient = ({damping_coeff:.7f} +/- {lambda_err:.7f}) cm^-1 (Q-factor = {Q_factor:.2f})")
    plt.legend()
    plt.show()


# Graph dispersion relation
plt.scatter(experimental_k.keys(), experimental_k.values())
plt.errorbar(experimental_k.keys(), experimental_k.values(), yerr=experimental_k_err.values())
# Predicted dispersion relation
def f_MHz(k_values, density):
    magnetic_field = 7e-3  # Teslas
    ion_mass = 39.948 / 1e3 / 6.023e23
    electron_mass_eV = 0.511e6
    electron_mass = 9.109e-31
    speed_of_light = 3e8
    electron_charge = 1.602e-19
    vacuum_permittivity = 8.854e-12
    electron_gyrofreq = magnetic_field * speed_of_light**2 / electron_mass_eV
    electron_plasma_freq = electron_charge * np.sqrt(density / electron_mass / vacuum_permittivity)
    electron_inertial_length = speed_of_light / electron_plasma_freq
    omega_values = [electron_gyrofreq / (1 + 1 / (k * electron_inertial_length)**2) for k in k_values]
    return [om / (2e6 * np.pi) for om in omega_values]
popt, cov = curve_fit(f_MHz, list(experimental_k.values()), list(experimental_k.keys()), p0=[4.3e17])
density = popt[0]
density_err = 2 * np.sqrt(cov[0, 0])
print(f"Density = {density} +/- {density_err}")
k_values = np.linspace(1, 160, 100)
best_fit = f_MHz(k_values, density)
plt.plot(best_fit, k_values, label=f"$n={density/1e17:.4f} \\times 10^{{17}}m^{{-3}}$")
plt.xlabel("$f=\\omega / 2 \\pi$ (MHz)")
plt.ylabel("$k$ ($m^{-1}$)")
plt.title("Experimental dispersion relation and best fit curve")
plt.legend()
plt.show()


for filename in xzplane_files:
    freq = 1e6 * int(filename.split("xzplane_")[1].split("MHz")[0])
    omega = freq * 2 * np.pi
    with h5py.File(filename, "r") as file:
        t = list(file["Acquisition/LeCroy_scope/time"])
        t -= t[0]
        positions_setup_array = list(file["Control/Positions/positions_setup_array"])
        z     = [bleh[1] for bleh in positions_setup_array]
        theta = [bleh[2] for bleh in positions_setup_array]
        dt = t[-1] / (len(t) - 1)
        # Voltage measured in each channel (before being amplified x10000)
        V_x = np.matrix(file["Acquisition/LeCroy_scope/Channel1"]) / 10000
        V_y = np.matrix(file["Acquisition/LeCroy_scope/Channel2"]) / 10000
        V_z = np.matrix(file["Acquisition/LeCroy_scope/Channel4"]) / 10000
        V_squared = np.multiply(V_x, V_x) + np.multiply(V_y, V_y) + np.multiply(V_z, V_z)
        V_rms = np.sqrt(np.mean(V_squared, axis=1))
        V_rms = V_rms.reshape(19, 55)
        fig = plt.imshow(V_rms * 1e3, cmap="plasma", extent=[z[0], z[-1], theta[-1], theta[0]], aspect="auto")
        plt.colorbar(fig)
        plt.xlabel("$z$ coordinate (cm)")
        plt.ylabel("$\\theta$ coordinate (degrees)")
        plt.title(f"RMS voltage measured from $\\dot{{B}}$ probe in mV\nover a 1.25ms period (f={int(freq/1e6)}MHz)")
        plt.show()
