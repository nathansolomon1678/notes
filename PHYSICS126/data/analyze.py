#!/usr/bin/env python3
import csv
from collections import defaultdict
from matplotlib import pyplot as plt
import math
from scipy.stats import linregress

columns = defaultdict(list)
with open("PDG.csv") as file:
    reader = csv.DictReader(file)
    for row in reader:
        for (k,v) in row.items():
            columns[k].append(math.log(float(v)))

# get lambda/A as a function of A, and X/A as a function of Z
columns["(nuclear interaction length divided by atomic mass)"] = [l-a for l,a in zip(columns["nuclear interaction length"], columns["atomic mass"])]
columns["(radiation length divided by atomic mass)"] = [x-a for x,a in zip(columns["radiation length"], columns["atomic mass"])]

def make_graph(x_key, y_key):
    plt.scatter(columns[x_key], columns[y_key])
    plt.xlabel(f"Natural log of {x_key}")
    plt.ylabel(f"Natural log of {y_key}")
    plt.title(f"Slope = {linregress(columns[x_key], columns[y_key]).slope:.5f}")
    plt.show()

make_graph("atomic mass", "(nuclear interaction length divided by atomic mass)")
make_graph("atomic number", "(radiation length divided by atomic mass)")
