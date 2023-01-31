

import numpy as np

drop_ones = lambda t: 0 if t <= 1 else 1

matrix_ocean = np.zeros([5, 5])

coords_ini = []
coords_end = []

with open('input.txt') as f:
    for i, line in enumerate(f):
        coords_string = line.split(" -> ")
        coords_ini.append(coords_string[0].split(","))
        coords_end.append(coords_string[1].split(","))
        
array_init = np.array(coords_ini).astype(int)
array_end = np.array(coords_end).astype(int)

max_corner = max(max(array_init[:, 0]), max(array_init[:, 1]), max(array_end[:, 0]), max(array_end[:, 1]))

matrix_ocean = np.zeros([max_corner + 10, max_corner + 10])

for coord_init, coord_end in zip(array_init, array_end):
    diff_coord = abs(coord_init - coord_end)
    if min(diff_coord) == 0:
        delta1 = 1
        delta2 = 1
        if coord_init[0] > coord_end[0]:
            delta1 = -1
        if coord_init[1] > coord_end[1]:
            delta2 = -1
        matrix_ocean[np.arange(coord_init[0], coord_end[0] + delta1, delta1), np.arange(coord_init[1], coord_end[1] + delta2, delta2)] += 1

matrix_ocean_zeros = np.vectorize(drop_ones)(matrix_ocean)
print(sum(sum(matrix_ocean_zeros)))


matrix_ocean = np.zeros([max_corner + 10, max_corner + 10])
for coord_init, coord_end in zip(array_init, array_end):
    diff_coord = abs(coord_init - coord_end)
    if min(diff_coord) == 0 or diff_coord[0] == diff_coord[1]:
        delta1 = 1
        delta2 = 1
        if coord_init[0] > coord_end[0]:
            delta1 = -1
        if coord_init[1] > coord_end[1]:
            delta2 = -1
        matrix_ocean[np.arange(coord_init[0], coord_end[0] + delta1, delta1), np.arange(coord_init[1], coord_end[1] + delta2, delta2)] += 1

matrix_ocean_zeros = np.vectorize(drop_ones)(matrix_ocean)
print(sum(sum(matrix_ocean_zeros)))