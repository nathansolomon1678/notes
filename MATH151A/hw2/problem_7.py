#!/usr/bin/env python3
from math import cos, sin

def f(x): return x + cos(x)

def f_prime(x): return 1 - sin(x)

def newtons_method(f, f_prime, p_0, tolerance, weird_version=False):
    if weird_version:
        print(f"\nVariation of Newton's method from problem 6")
    else:
        print(f"\nNewton's method")
    print(f"{p_0=}\t{tolerance=}\n{'='*53}")
    i = 0
    p = p_0
    while abs(f(p)) > tolerance:
        i += 1
        if weird_version:
            p -= f(p) / f_prime(p_0)
        else:
            p -= f(p) / f_prime(p)
        print(f"p_{i:02} = {p:>16.15f},  residual = {abs(f(p)):>16.15f}")

def secant_method(f, p_0, p_1, tolerance):
    print(f"\nSecant method")
    print(f"{p_0=}\t{p_1=}\t{tolerance=}\n{'='*53}")
    p = [p_0, p_1]
    while abs(f(p[-1])) > tolerance:
        p.append((p[-2]*f(p[-1])-p[-1]*f(p[-2])) / (f(p[-1])-f(p[-2])))
    for i in range(len(p)):
        print(f"p_{i:02} = {p[i]:>16.15f},  residual = {abs(f(p[i])):>16.15f}")

newtons_method(f, f_prime, -5, 1e-10)
secant_method(f, -5, 5, 1e-10)
newtons_method(f, f_prime, -.9, 1e-10)
newtons_method(f, f_prime, -.9, 1e-10, weird_version=True)
secant_method(f, -.9, 5, 1e-10)
