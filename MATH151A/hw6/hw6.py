#!/usr/bin/env python3

### # Problem 4
### import math
### 
### def f(x):
###     return math.sin(x)
### def f_prime_exact(x):
###     return math.cos(x)
### def f_prime_approx(x, h):
###     return (f(x) - f(x - h)) / h
### 
### x = math.pi / 3
### print(f"{x=:.8f}  {f_prime_exact(x)=:.8f}\n")
### for h in [.1, .01, .001]:
###     absolute_error = abs(f_prime_exact(x) - f_prime_approx(x, h))
###     print(f"{h=:.3f}  {f_prime_approx(x, h)=:.8f}  {absolute_error=:.8f}")


# Problem 6
import math
import numpy as np
import matplotlib.pyplot as plt

def f(x):
    return x * x * math.log(x)
def f_prime_approx(x, h):
    return (f(x + h) - f(x)) / h
def f_prime_exact(x):
    return 2 * x * math.log(x) + x
def absolute_error(x, h):
    return abs(f_prime_exact(x) - f_prime_approx(x, h)) / f_prime_exact(x)

x_vals = 10 ** np.linspace(-10, 0, 500)
y_vals = [absolute_error(2, h) for h in x_vals]

best_h = x_vals[y_vals.index(min(y_vals))]
print(f"Absolute error is minimized when h = {best_h}")

plt.plot(x_vals, y_vals)
plt.xlabel("h")
plt.ylabel("absolute error")
plt.xscale("log")
plt.yscale("log")
plt.show()
