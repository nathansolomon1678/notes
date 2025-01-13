#!/usr/bin/env python3

from random import choice
import time
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from math import log

# Given two numbers as strings of digits 0-9, returns their sum as a string
def add_strings(a, b, actually_do_subtraction_instead=False):
    # If doing subtraction, assume a >= b
    assert a.isdigit() and b.isdigit()
    digits_of_sum = []
    carry_digit = 0
    for i in range(max(len(a), len(b))):
        digit1 = a[len(a) - i - 1] if i < len(a) else 0
        digit2 = b[len(b) - i - 1] if i < len(b) else 0
        if actually_do_subtraction_instead:
            total = carry_digit + int(digit1) - int(digit2)
        else:
            total = carry_digit + int(digit1) + int(digit2)
        carry_digit = total // 10
        digits_of_sum.insert(0, str(total % 10))
    digits_of_sum.insert(0, str(carry_digit))
    digits_of_sum = ''.join(digits_of_sum).lstrip('0')
    if digits_of_sum == "":
        return '0'
    return digits_of_sum

# Given two numbers as strings of digits 0-9, returns their product as a string
def multiply_strings(x, y):
    assert x.isdigit() and y.isdigit()
    # Left pad with zeros until they are the same length, for convenience
    if len(x) > len(y):
        y = '0' * (len(x) - len(y)) + y
    if len(x) < len(y):
        x = '0' * (len(y) - len(x)) + x
    n = len(x)
    # If there are less than two digits left to multiply, just calculate the product normally
    if n == 0:
        return 0
    if n == 1:
        return str(int(x) * int(y))
    # If the numbers still have more than one digit, use Karatsuba multiplication
    m = n // 2

    x_0 = x[-m:]
    x_1 = x[:-m]
    y_0 = y[-m:]
    y_1 = y[:-m]

    z_0 = multiply_strings(x_0, y_0)
    z_2 = multiply_strings(x_1, y_1)
    z_3 = multiply_strings(add_strings(x_0, x_1), add_strings(y_0, y_1))
    z_1 = add_strings(z_3, add_strings(z_0, z_2), actually_do_subtraction_instead=True)
    z_2 += '0' * 2 * m
    z_1 += '0' * m
    return add_strings(z_0, add_strings(z_1, z_2))

def rand_int_string(num_digits):
    valid_digits = list("0123456789")
    return ''.join([choice(valid_digits) for i in range(num_digits)])

def computation_time(n):
    assert n > 0
    x = rand_int_string(n)
    y = rand_int_string(n)
    start_time = time.time()
    z = multiply_strings(x, y)
    return time.time() - start_time

x_values = list(range(1, 100, 1))
y_values = []
for n in x_values:
    run_time = computation_time(n)
    y_values.append(run_time)

plt.scatter(x_values, y_values, label="Computation time", alpha=0.5)

def f(x_values, constant, power):
    return [constant * x ** power for x in x_values]
def g(x_values, constant):
    return f(x_values, constant, log(3, 2))

constant, power = curve_fit(f, x_values, y_values, p0=[1, 1.58])[0]
print(f"Best fit curve:  t is proportional to n ^ {power}")
print(f"Expected result: t is proportional to n ^ {log(3, 2)}")
plt.plot(x_values, f(x_values, constant, power), label=f"$t \propto n \^ {power:.5f}$ (best fit curve)", color="green")

constant = curve_fit(g, x_values, y_values)[0][0]
plt.plot(x_values, g(x_values, constant), label=f"$t \propto n \^ (\log_2 3) \\approx n \^ {log(3, 2):.5f}$", color="purple")

plt.title("Karatsuba algorithm run time")
plt.xlabel("n = number of digits")
plt.ylabel("t = run time (seconds)")
plt.legend()
plt.show()
