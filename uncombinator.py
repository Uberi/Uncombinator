#!/usr/bin/env python3

"""
from . import bayes

c = bayes.Classifier()

c.observe("Nobody owns the water.","good")
c.observe("the quick rabbit jumps fences","good")
c.observe("buy pharmaceuticals now","bad")
c.observe("make quick money at the online casino","bad")
c.observe("the quick brown fox jumps","good")

print(c.classify("quick rabbit"))
"""

import math
    
def read_tuples_of_4(file_object):
    values = (int(value) for value in file_object.readlines())
    return [((value // 1000) % 10, (value // 100) % 10, (value // 10) % 10, value % 10) for value in values]

def chronological_clean(tuples): # remove duplicates when there are no changes to the system, in order to maintain correct weightings for each hidden data point
    result = []
    previous = None
    for value in tuples:
        if value != previous: result.append(value)
        previous = value
    return result

def mean_and_standard_deviation(data):
    count = len(data)
    data = [(x + 10 if x < 5 else x) for x in data]
    mean = sum(data) / count # wip: dirty hack
    standard_deviation = math.sqrt(sum((x - mean) ** 2 for x in data) / count)
    return mean, standard_deviation

hidden = chronological_clean(read_tuples_of_4(open("hidden_data.txt", "r"))) # lock position after the target scrambles the lock starting from the combination
known = read_tuples_of_4(open("known_data.txt", "r")) # offsets of the lock after we scramble the lock starting from 0000

# calculate known variance and expected value
known_expected_values, known_standard_deviations = tuple(zip(*(mean_and_standard_deviation(values) for values in zip(*known))))
hidden_expected_values, hidden_standard_deviations = tuple(zip(*(mean_and_standard_deviation(values) for values in zip(*hidden))))

print("EXPECTED VALUES/STANDARD DEVIATIONS:")
print("HIDDEN: ", hidden_expected_values, hidden_standard_deviations)
print("KNOWN: ", known_expected_values, known_standard_deviations)

expected_combination = tuple((x - y) % 10 for x, y in zip(hidden_expected_values, known_expected_values))
expected_standard_deviations = tuple(math.sqrt(x ** 2 + y ** 2) for x, y in zip(hidden_standard_deviations, known_standard_deviations))

print("EXPECTED COMBINATION/COMBINATION STANDARD DEVIATION:")
print(expected_combination, expected_standard_deviations)

print("========================= THE COMBINATION IS PROBABLY {} =========================".format("".join(str(int(x + 0.5)) for x in expected_combination)))
print(", ".join(str(int(x + 0.5)) + "+-" + str(int(y + 0.5)) for x, y in zip(expected_combination, expected_standard_deviations)))

import matplotlib.pyplot as plt

plt.figure(figsize=(8, 6))
plt.boxplot([
    [expected_combination[0] - expected_standard_deviations[0], expected_combination[0], expected_combination[0] + expected_standard_deviations[0]],
    [expected_combination[1] - expected_standard_deviations[1], expected_combination[1], expected_combination[1] + expected_standard_deviations[1]],
    [expected_combination[2] - expected_standard_deviations[2], expected_combination[2], expected_combination[2] + expected_standard_deviations[2]],
    [expected_combination[3] - expected_standard_deviations[3], expected_combination[3], expected_combination[3] + expected_standard_deviations[3]]
], showbox=False, labels=["1", "2", "3", "4"])
for i in range(4): plt.gca().annotate("{:.3f}".format(expected_combination[i]), xy=(i + 1, expected_combination[i] + 0.05), ha="center")
plt.xlabel("Digit Position")
plt.ylabel("Value")
plt.title("Lock Combination")
plt.grid()
plt.show()