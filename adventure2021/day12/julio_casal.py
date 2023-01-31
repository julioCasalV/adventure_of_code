
import numpy as np
import itertools as it
import re

list_points = np.loadtxt('input.txt', delimiter = "-", dtype='str')

list_unique_point = np.unique(list_points)

dicc_point = {}
for item in list_unique_point:
    relations = list_points[(list_points == item).any(axis=1)].copy()
    relations = np.unique(relations)
    relations = relations[relations != item]
    relations = relations[relations != 'start']
    dicc_point[item] = relations

count = 0
list_previous = [{'seq' : ['start'], 'posibilities' : list(list_unique_point[list_unique_point != 'start'])}]

while len(list_previous) > 0:
    list_current = []
    for item in list_previous:
        seq_orig = item['seq'].copy()
        posibilities_orig = item['posibilities'].copy()
        point_last = seq_orig[-1]
        for point_next in dicc_point[point_last]:
            if point_next in posibilities_orig:
                if point_next == 'end':
                    count += 1
                else:
                    posibilities = posibilities_orig.copy()
                    seq = seq_orig.copy()
                    seq.append(point_next)
                    if np.char.lower(point_next) == point_next:
                        posibilities.remove(point_next)
                    list_current.append({'seq' : seq, 'posibilities' : posibilities})
    list_previous = list_current.copy()
print(count)


list_unique_point_upper = [item for item in list_unique_point if np.char.upper(item) == item]
list_unique_point_lower = [item for item in list_unique_point if np.char.lower(item) == item and item != 'start' and item != 'end']



count = 0
list_previous = [{'seq' : ['start'], 'posibilities' : (list_unique_point_upper + list_unique_point_lower + list_unique_point_lower + ['end'])}]

while len(list_previous) > 0:
    list_current = []
    for item in list_previous:
        seq_orig = item['seq'].copy()
        posibilities_orig = item['posibilities'].copy()
        point_last = seq_orig[-1]
        for point_next in dicc_point[point_last]:
            if point_next in posibilities_orig:
                if point_next == 'end':
                    count += 1
                else:
                    posibilities = posibilities_orig.copy()
                    seq = seq_orig.copy()
                    seq.append(point_next)
                    if np.char.lower(point_next) == point_next:
                        posibilities.remove(point_next)
                        if point_next not in posibilities:
                            posibilities = list(np.unique(posibilities))
                            list_used = [item for item in seq if np.char.lower(item) == item]
                            posibilities = [item for item in posibilities if item not in list_used]
                    list_current.append({'seq' : seq, 'posibilities' : posibilities})
    list_previous = list_current.copy()
print(count)