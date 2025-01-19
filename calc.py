#!/usr/bin/env python3

""" To use this calculator, run the python3 interpreter and import * from this file,
then enter your calculations with regular python syntax. EXAMPLE:

>>> from calc import *
>>> eV / K
11605
>>> J / c**2
$1.1127 \times 10^{-17} \si{. kg}$
1.1127 × 10⁻¹⁷ kg

Note that this calculator should not be used for advanced calculations, but
it can work well for arithmetic and powers (+, -, *, /, and **)
"""
# TODO: rename all variable names so that they cannot possibly collide with
# other variable names. For example, nowhere in this code should I use a
# variable called "value" or "k" or any other common name like that. Also,
# resolve ambiguity around constants like "e" (euler's constant, not
# fundamental charge) and "C" (coulomb, not speed of light)
# TODO: also keep track of Coulombs, in addition to m, kg, and s
# TODO: confirm that scalar division and other basic operations work as they should
# TODO: add a nicer way to change the global settings

##################################################
# GLOBAL SETTINGS:
digits_of_precision = 5
natural_units = False
scientific_notation = False
##################################################

from math import *

class Fraction:
    # Represents a rational number
    # n is the numerator, d is the denominator
    # Does not allow you to do regular math that you could do with real numbers,
    # such as multiplying by a scalar, or raising to a non-integer power
    def __init__(self, n, d):
        if d == 0 or not isinstance(n, int) or not isinstance(d, int):
            raise ValueError("Numerator and denominator must both be integers, and denominator cannot be zero")
        self.n = n
        self.d = d
    def reduce(self):
        assert self.n == int(self.n)
        assert self.d == int(self.d)
        greatest_common_divisor = gcd(self.n, self.d)
        self.n /= greatest_common_divisor
        self.d /= greatest_common_divisor
        self.n = int(self.n)
        self.d = int(self.d)
        if self.d < 0:
            self.n *= -1
            self.d *= -1
    def __mul__(self, other):
        if not isinstance(other, Fraction):
            raise ValueError("I have not yet implemented multiplication between fractions and other types")
        return Fraction(self.n * other.n, self.d * other.d)
    def __add__(self, other):
        if not isinstance(other, Fraction):
            raise ValueError("I have not yet implemented addition between fractions and other types")
        return Fraction(self.n * other.d + self.d * other.n, self.d * other.d)
    def __sub__(self, other):
        return self + (other * Fraction(-1, 1))
    def __pow__(self, other):
        return Fraction(self.n ** other, self.d ** other)
    def __truediv__(self, other):
        return self * (other ** -1)
    def __repr__(self):
        self.reduce()
        if self.d == 1:
            return str(int(self.n))
        return f"({self.n}/{self.d})"
    def __eq__(self, other):
        self.reduce()
        other.reduce()
        return self.n == other.n and self.d == other.d

def superscript(string):
    string = str(string)
    characters = []
    for character in string:
        assert character in "-0123456789"
        if character == '-':
            characters.append('⁻')
        else:
            characters.append("⁰¹²³⁴⁵⁶⁷⁸⁹"[int(character)])
    return "".join(characters)

class Quantity:
    def __init__(self, value, pow_m, pow_kg, pow_s):
        self.value = value
        # Allow powers of m, kg, and s to be defined as either integers or Fractions
        self.pow_m  = Fraction(pow_m , 1) if isinstance(pow_m , int) else pow_m
        self.pow_kg = Fraction(pow_kg, 1) if isinstance(pow_kg, int) else pow_kg
        self.pow_s  = Fraction(pow_s , 1) if isinstance(pow_s , int) else pow_s
    def reduce_all(self):
        self.pow_m.reduce()
        self.pow_kg.reduce()
        self.pow_s.reduce()
    def units_match(self, other):
        self.reduce_all()
        other.reduce_all()
        return self.pow_m == other.pow_m and self.pow_kg == other.pow_kg and self.pow_s == other.pow_s
    def __add__(self, other):
        assert units_match(self, other)
        return Quantity(self.value + other.value, self.pow_m, self.pow_kg, self.pow_s)
    def __rmul__(self, other):
        if isinstance(other, float):
            return Quantity(self.value * other, self.pow_m, self.pow_kg, self.pow_s)
    def __mul__(self, other):
        if isinstance(other, float):
            return Quantity(self.value * other, self.pow_m, self.pow_kg, self.pow_s)
        return Quantity(
                self.value  * other.value,
                self.pow_m  + other.pow_m,
                self.pow_kg + other.pow_kg,
                self.pow_s  + other.pow_s)
    def __pow__(self, other):
        return Quantity(
                self.value ** other,
                self.pow_m  * Fraction(other, 1),
                self.pow_kg * Fraction(other, 1),
                self.pow_s  * Fraction(other, 1))
    def __truediv__(self, other):
        return self * (other ** -1)
    def __repr__(self):
        scalar_value = self.value
        powers = {
                "eV"  : Fraction(0, 1),
                "hbar": Fraction(0, 1),
                "c"   : Fraction(0, 1),
                "m"   : self.pow_m,
                "kg"  : self.pow_kg,
                "s"   : self.pow_s
        }
        if natural_units:
            powers["eV"]   = powers["kg"] - powers["m"] - powers["s"]
            powers["hbar"] = powers["m"] + powers["s"]
            powers["c"]    = powers["m"] - Fraction(2, 1) * powers["kg"]
            powers["m"]  = Fraction(0, 1)
            powers["kg"] = Fraction(0, 1)
            powers["s"]  = Fraction(0, 1)
            # The quantities eV, hbar, and c are defined below
            scalar_value /=   eV.value ** (powers["eV"  ].n / powers["eV"  ].d)
            scalar_value /= hbar.value ** (powers["hbar"].n / powers["hbar"].d)
            scalar_value /=    c.value ** (powers["c"   ].n / powers["c"   ].d)
        for key in powers.keys():
            powers[key].reduce()
        exponent = floor(log10(scalar_value))
        scalar_value /= 10 ** exponent
        scalar_value = round(scalar_value, digits_of_precision - 1)
        if scientific_notation or 'e' in (scalar_value * 10 ** exponent).__repr__():
            output_string = f"{scalar_value} × 10{superscript(exponent)}"
            output_latex = f"${scalar_value} \\times 10^{{{exponent}}} \\si{{."
        else:
            scalar_value *= 10 ** exponent
            if scalar_value == int(scalar_value):
                scalar_value = int(scalar_value)
            output_string = str(scalar_value)
            output_latex  = f"${scalar_value} \\si{{."
        for key, value in powers.items():
            if value == Fraction(0, 1):
                continue
            elif value == Fraction(1, 1):
                output_string += f" {key}"
                output_latex += f" {key}"
            elif value.d == 1:
                output_string += f" {key}{superscript(value.n)}"
                output_latex += f" {key}^{{{value.n}}}"
            else:
                output_string += f" {key}^{value}"
                output_latex += f" {key}^{{{value}}}"
        output_latex += "}$"
        # If quantity is dimensionless, don't bother printing the LaTeX
        if " \si{.}" not in output_latex:
            print(output_latex)
        return output_string

# ESSENTIAL CONSTANTS
m  = Quantity(1, 1, 0, 0)
kg = Quantity(1, 0, 1, 0)
s  = Quantity(1, 0, 0, 1)

i = 1j

eV   = Quantity(1.602176634e-19, 2, 1, -2)
hbar = Quantity(1.054571817e-34, 2, 1, -1)
c    = Quantity(299792458      , 1, 0, -1)

# OTHER CONSTANTS AND UNIT CONVERSIONS

N = m * kg / s**2 # Newton
J = m * N # Joule
K = 1.380649e-23 * J # degree Kelvin (assuming Boltzmann's constant is 1)
mol = 6.02214076e23 # Avogadro's number

# mass of electron (call it q_e)
# rydberg constant
# fine structure constant
# charge of electron
# permittivity of free space
# TODO: define atmosphere, torr, mmHg, and other obscure units
