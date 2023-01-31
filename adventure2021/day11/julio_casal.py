'''
Created on 1 feb. 2022

@author: ASOL
'''

import numpy as np

data_list = []
with open('input.txt') as f:
    for line in f:
        data_list.append(list(line.split()[0]))

data = np.ones([12, 12])*10
data[1:11, 1:11] = np.array(data_list).astype(int)

data_ones_orig = np.zeros([12, 12])
data_ones_orig[1:11, 1:11] = np.ones([10, 10])

total = 0
for bucle in range(100):
    data_ones = data_ones_orig.copy()
    data += 1
    while True:
        data_flash = (data > 9).astype(int)*data_ones
        data_ones = data_ones - data_flash
        list_coord = np.argwhere(data_flash == 1)
        if list_coord.shape[0] < 1:
            break
        for [i, j] in list_coord:
            data[i-1:i+2, j-1:j+2] += 1
        total += list_coord.shape[0]
    data[1:11, 1:11][data[1:11, 1:11]>9] = 0
print(total)


data = np.ones([12, 12])*10
data[1:11, 1:11] = np.array(data_list).astype(int)

for bucle in range(112500):
    data_ones = data_ones_orig.copy()
    data += 1
    while True:
        data_flash = (data > 9).astype(int)*data_ones
        data_ones = data_ones - data_flash
        list_coord = np.argwhere(data_flash == 1)
        if list_coord.shape[0] < 1:
            break
        for [i, j] in list_coord:
            data[i-1:i+2, j-1:j+2] += 1
    data[1:11, 1:11][data[1:11, 1:11]>9] = 0
    if np.count_nonzero(data[1:11, 1:11]) == 0:
        print(bucle+1)
        break
