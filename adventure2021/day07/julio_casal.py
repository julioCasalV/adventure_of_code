
import numpy as np



data = np.genfromtxt('input.txt', delimiter=',')
unique, counts = np.unique(data, return_counts=True)
total = sum(data)
posibilities_list = np.arange(min(unique), max(unique) +1)
for item in posibilities_list:
    total_fuel = sum(abs(data-item))
    if total_fuel < total:
        total = total_fuel
print(total)

total = sum(data)*100000
for item in posibilities_list:
    resta = abs(data-item)
    total_fuel = sum(resta*(resta+1)/2)
    if total_fuel < total:
        total = total_fuel
print(total)