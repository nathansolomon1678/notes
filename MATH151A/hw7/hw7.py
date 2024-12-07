#!/usr/bin/env python3
from math import exp, sqrt, pi

x = 0.5
N = 50
def f(x):
    summation = 0
    for j in range(N):
        summation += exp(0 - (j    *x/N)**2 / 2)
        summation += exp(0 - ((j+1)*x/N)**2 / 2)
    return -0.45 + summation * x / (2 * N * sqrt(2 * pi))

for i in range(100):
    print(f"x_{i} = {x}")
    residual = f(x)
    if abs(residual) < 1e-5:
        break
    x -= sqrt(2 * pi) * exp(x**2 / 2) * residual
