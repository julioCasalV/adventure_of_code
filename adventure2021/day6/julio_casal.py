
import numpy as np

begin_again = lambda t: 6 if t == -1 else t

total_days = 80
data = np.genfromtxt('input.txt', delimiter=',')
unique, counts = np.unique(data, return_counts=True)
total = 0
for orig, count_orig in zip(unique, counts):
    lanternfish_list = np.array([orig])
    for day in range(80):
        lanternfish_list -= 1
        unique, counts = np.unique(lanternfish_list, return_counts=True)
        if unique[0] == -1:
            lanternfish_list = np.append(lanternfish_list, np.ones(counts[0])*8)
            lanternfish_list = np.vectorize(begin_again)(lanternfish_list)
    total += len(lanternfish_list)*count_orig

print(total)

unique, counts = np.unique(data, return_counts=True)
lanternfish_list = dict(zip(unique, counts))
fish_list_zeros = dict(zip(np.arange(0,9), np.zeros(9)))
for day in range(256):
    lanternfish_list_day = fish_list_zeros.copy()
    for item in lanternfish_list:
        item_next = item - 1
        if item_next == -1:
            lanternfish_list_day[8] += lanternfish_list[item]
            item_next = 6
        lanternfish_list_day[item_next] += lanternfish_list[item]
    lanternfish_list = lanternfish_list_day.copy()
            

print(sum(lanternfish_list.values()))