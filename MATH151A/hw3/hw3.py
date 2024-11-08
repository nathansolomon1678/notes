#!/usr/bin/env python3

### # Problem 2
### import math
### 
### def f(x):
###     return math.exp(x) - 1 - x - x**2/2
### def f_prime(x):
###     return math.exp(x) - 1 - x
### def f_prime_prime(x):
###     return math.exp(x) - 1
### def mu(x):
###     return f(x) / f_prime(x)
### def mu_prime(x):
###     return 1 - f(x) * f_prime_prime(x) / f_prime(x)**2
### 
### def newtons_method(x_0, tolerance, max_iterations):
###     print(f"\nNewton's method with {x_0=}, {tolerance=}, {max_iterations=}")
###     x_n = x_0
###     n = 0
###     residual = abs(f(x_n))
###     print(f"{n=:02}  {x_n=:+1.8f}  {residual=:1.17f}")
###     while abs(x_n) > tolerance and n < max_iterations:
###         x_n -= f(x_n) / f_prime(x_n)
###         n += 1
###         residual = abs(f(x_n))
###         print(f"{n=:02}  {x_n=:+1.8f}  {residual=:1.17f}")
### 
### def modified_newtons_method(x_0, tolerance, max_iterations):
###     print(f"\nModified Newton's method with {x_0=}, {tolerance=}, {max_iterations=}")
###     x_n = x_0
###     n = 0
###     residual = abs(f(x_n))
###     print(f"{n=:02}  {x_n=:+1.8f}  {residual=:1.17f}")
###     while abs(x_n) > tolerance and n < max_iterations:
###         x_n -= mu(x_n) / mu_prime(x_n)
###         n += 1
###         residual = abs(f(x_n))
###         print(f"{n=:02}  {x_n=:+1.8f}  {residual=:1.17f}")
### 
### newtons_method(1, 1e-10, 1000)
### modified_newtons_method(1, 1e-10, 1000)


### # Problem 3
### p = 1
### def p(n):
###     return 1 + 1 / n
### def p_hat(n):
###     return p(n) - (p(n+1) - p(n))**2 / (p(n+2) - 2 * p(n+1) + p(n))
### 
### for n in range(1, 8):
###     print(f"{n=} {p(n)=:1.5f} {p_hat(n)=:1.5f}")


### # Problem 4
### import math
### def P(x):
###     return math.log(2) * (-x**2+4*x-3) + math.log(3) * (x**2-3*x+2)/2
### print(f"{P(1)=}")
### print(f"{P(2)=}")
### print(f"{P(3)=}")
### print(f"{P(1.5)=}")
### print(f"{P(2.4)=}")
### 
### def error(x):
###     return abs(P(x) - math.log(x))
### import numpy as np
### for x in np.linspace(1,3,100):
###     print(f"{x=:1.5f} {error(x)=:1.5f}")
### print('\n')
### # x=1.34343 error(x)=0.02474
### # x=1.36364 error(x)=0.02482
### # x=1.38384 error(x)=0.02479
### for x in np.linspace(1.34,1.39,100):
###     print(f"{x=:1.5f} {error(x)=:1.10f}")
### # x=1.36677 error(x)=0.0248176530
### # x=1.36727 error(x)=0.0248177110
### # x=1.36778 error(x)=0.0248177061

# Problem 5
import numpy as np
# x is years since 1960, y is United States population (in thousands)
x = [0, 10, 20, 30, 40, 50]
y = [179_323, 203_302, 226_542, 249_633, 281_422, 308_746]
N = 5
assert len(x) == N + 1 and len(y) == N + 1
V = np.vander(x, N+1)
coeffs = np.linalg.inv(V) @ np.matrix([y]).T
print("P(x) = " + " ".join([f"{coeffs[i, 0]:+} x^{N-i}" for i in range(N+1)]))
def P(x):
    return round((np.matrix([[x**(N-i) for i in range(N+1)]]) @ coeffs)[0, 0])
for x in [0, 10, 20, 30, 40, 50, 60]:
    print(f"year {1960+x}: {P(x)=:6}")
actual_value = 329_500
print(f"Relative error: {abs(P(60) - actual_value) / actual_value}")
