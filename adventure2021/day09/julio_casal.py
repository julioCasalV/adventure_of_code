'''
Created on 27 ene. 2022

@author: ASOL
'''
import numpy as np

def count_basin(x_coord, y_coord):
    list_coord = [[x_coord, y_coord]]
    list_coord_total = [[x_coord, y_coord]]
    while len(list_coord) > 0:
        list_coord_next = []
        for [i, j] in list_coord:
            num_compare = data[i, j] + 1
            if num_compare == 9:
                num_compare = 100
            if i > 0 and [i-1, j] not in list_coord_total and data[i-1, j] in np.arange(data[i, j], 9):
                list_coord_next.append([i-1, j])
            if i < data.shape[0]-1 and [i+1, j] not in list_coord_total  and data[i+1, j] in np.arange(data[i, j], 9):
                list_coord_next.append([i+1, j])
            if j > 0 and [i, j-1] not in list_coord_total  and data[i, j-1] in np.arange(data[i, j], 9):
                list_coord_next.append([i, j-1])
            if j < data.shape[1]-1 and [i, j+1] not in list_coord_total  and data[i, j+1] in np.arange(data[i, j], 9):
                list_coord_next.append([i, j+1])
        list_coord = []
        [list_coord.append(x) for x in list_coord_next if x not in list_coord]
        [list_coord_total.append(x) for x in list_coord if x not in list_coord_total]
    total = len(list_coord_total)
    return total

data_list = []
with open('input.txt') as f:
    for i, line in enumerate(f):
        data_list.append(list(line.split()[0]))

data = np.array(data_list).astype(int)
total = 0
for i in range(data.shape[0]):
    for j in range(data.shape[1]):
        num_compare = data[i, j]
        incr = 1
        if i > 0 and data[i-1, j] <= num_compare:
            incr = 0
        if i < data.shape[0]-1 and data[i+1, j] <= num_compare:
            incr = 0
        if j > 0 and data[i, j-1] <= num_compare:
            incr = 0
        if j < data.shape[1]-1 and data[i, j+1] <= num_compare:
            incr = 0
        total += incr*(num_compare + 1)
print(total)

list_total_basin = []
list_total_basin_repeat = []
list_basin = []
for i in range(data.shape[0]):
    for j in range(data.shape[1]):
        num_compare = data[i, j]
        incr = 1
        if i > 0 and data[i-1, j] <= num_compare:
            incr = 0
        if i < data.shape[0]-1 and data[i+1, j] <= num_compare:
            incr = 0
        if j > 0 and data[i, j-1] <= num_compare:
            incr = 0
        if j < data.shape[1]-1 and data[i, j+1] <= num_compare:
            incr = 0
        if incr == 1:
            list_basin.append(count_basin(i, j))

list_basin = np.sort(list_basin)
print(np.prod(list_basin[-3:]))
