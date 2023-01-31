import numpy as np
import time

y_min = -267

regexp = r"target area: x=(\d+)\.\.(\d+), y=(-\d+)\.\.(-\d+)"
out = np.fromregex('input.txt', regexp, [('x_min', np.int64),('x_max', np.int64), ('y_min', np.int64), ('y_max', np.int64)])
x_max = out['x_max']
x_min = out['x_min']
y_max = out['y_max']
y_min = out['y_min']


y_max_high = (np.abs(y_min)-1)*np.abs(y_min)/2

print(y_max_high)

x_min_init_vel = int(np.sqrt(x_min*2)-1)
x_max_init_vel = x_max

y_min_init_vel = y_min
y_max_init_vel = np.abs(y_min)-1

count = 0
list = []

for x in np.arange(x_min_init_vel, x_max_init_vel + 1):
    steps = -1
    for x_cal in np.arange(x-1, -1000, -1):
        steps = steps + 1
        x_cal = np.sum(np.arange(x, max(x_cal, -1), -1))
        if x_cal > x_max:
            break
        elif x_cal < x_min:
            continue
        for y in np.arange(y_max_init_vel, y_min_init_vel - 1,  -1):
            y_cal = y - steps - 1
            y_cal = np.sum(np.arange(y, y_cal, -1))
            if y_cal < y_min:
                break
            elif y_cal >= y_min and y_cal <= y_max:
                list.append(f'{x},{y}')

list_uniq = np.unique(list)
print(len(list_uniq))