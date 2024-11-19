#!/usr/bin/env python3

### # Problem 1
### import numpy as np
### import math
### import matplotlib.pyplot as plt
### 
### def f(x):
###     return math.sin(2 * math.pi * x)
### 
### def P(n, x):
###     m = math.floor(n * x)
###     fract = n * x - m
###     return f(m / n) + fract * (f((m+1) / n) - f(m / n))
### 
### x_data = np.linspace(0, 1, 400)
### plt.plot(x_data, [f(x) for x in x_data])
### for n in [2, 4, 8]:
###     y_data = [P(n, x) for x in x_data]
###     plt.plot(x_data, y_data)
### plt.show()

### # Problem 3
### import scipy.integrate as integrate
### import numpy as np
### 
### A = np.matrix([
###     [.001, .01, .1, 1,    0,   0,  0, 0],
###     [.008, .04, .2, 1,    0,   0,  0, 0],
###     [   0,   0,  0, 0, .008, .04, .2, 1],
###     [   0,   0,  0, 0, .027, .09, .3, 1],
###     [  .6,   2,  0, 0,    0,   0,  0, 0],
###     [   0,   0,  0, 0,  1.8,   2,  0, 0],
###     [ .12,  .4,  1, 0, -.12, -.4, -1, 0],
###     [ 1.2,   2,  0, 0, -1.2,  -2,  0, 0]
### ])
### B = np.matrix([[-0.29004996, -0.56079734, -0.56079734, -0.81401972, 0, 0, 0, 0]]).T
### 
### X = np.linalg.inv(A) @ B
### a_0 = X[0, 0]
### b_0 = X[1, 0]
### c_0 = X[2, 0]
### d_0 = X[3, 0]
### a_1 = X[4, 0]
### b_1 = X[5, 0]
### c_1 = X[6, 0]
### d_1 = X[7, 0]
### print(f"{a_0=}\n{b_0=}\n{c_0=}\n{d_0=}\n\n{a_1=}\n{b_1=}\n{c_1=}\n{d_1=}")
### 
### def f(x):
###     return x**2 * np.cos(x) - 3 * x
### def f_prime(x):
###     return 2 * x * np.cos(x) - x**2 * np.sin(x) - 3
### def s(x):
###     if x < 0.2:
###         return a_0 * x**3 + b_0 * x**2 + c_0 * x + d_0
###     return     a_1 * x**3 + b_1 * x**2 + c_1 * x + d_1
### def s_prime(x):
###     if x < 0.2:
###         return 6 * a_0 * x**2 + 2 * b_0 * x + c_0
###     return     6 * a_1 * x**2 + 2 * b_1 * x + c_1
### 
### print(f"\n{f(0.18)=}")
### print(f"{s(0.18)=}")
### print(f"Relative error = {abs((f(0.18) - s(0.18)) / f(0.18))}")
### print(f"\n{f_prime(0.18)=}")
### print(f"{s_prime(0.18)=}")
### print(f"Relative error = {abs((f_prime(0.18) - s_prime(0.18)) / f_prime(0.18))}")
### 
### print(f"\n{f(0.2)=}\n{s(0.2)=}")
### 
### exact_integral  = integrate.quad(f, 0.1, 0.3)[0]
### approx_integral = integrate.quad(s, 0.1, 0.3)[0]
### print(f"\n{exact_integral=}")
### print(f"{approx_integral=}")
### print(f"Relative error = {abs((exact_integral - approx_integral) / approx_integral)}")


# Problem 4
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import CubicSpline

def f(a, x):
    return np.cos(a * x) * x**2 + 10 * x

xvals = np.linspace(0, 10, 15)
x_points = np.linspace(0, 10, 500)

for a in [1, 3, 5]:
    fvals = [f(a, x) for x in xvals]
    plt.scatter(xvals, fvals)
    spln = CubicSpline(xvals, fvals)
    y_points = [f(a, x) for x in x_points]
    plt.plot(x_points, y_points)
    y_points = [spln(x) for x in x_points]
    plt.plot(x_points, y_points)
    plt.title(f"{a=}")
    plt.show()
