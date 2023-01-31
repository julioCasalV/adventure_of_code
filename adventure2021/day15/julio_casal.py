import numpy as np
import time

start_time = time.time()

list_points = np.loadtxt('input.txt', dtype='str')

list_point_tmp = []
for item in list_points:
    list_point_tmp.append(list(item))


list_points_cal = np.array(list_point_tmp).reshape(len(list_points), -1).astype(int)

list_points = list_points_cal

repetition = 4

for i in range(repetition):
    list_points_cal = np.vectorize(lambda x: x if x < 10 else 1)(list_points_cal + 1)
    list_points = np.concatenate((list_points, list_points_cal))
list_points_cal = list_points
for i in range(repetition):
    list_points_cal = np.vectorize(lambda x: x if x < 10 else 1)(list_points_cal + 1)
    list_points = np.concatenate((list_points, list_points_cal), axis = 1)


def calculate_risk_up(level, list_current_risk, list_current_updates):
    for item in np.arange(1, level*2):
        list_current_risk[item] = np.min([list_current_risk[item-1]+list_current_updates[item], list_current_risk[item]])
    for item in np.arange(level*2 - 1, -1, -1):
        list_current_risk[item] = np.min([list_current_risk[item+1]+list_current_updates[item], list_current_risk[item]])
    return list_current_risk

def calculate_risk_down(level, list_current_risk, list_next_risk, list_current_updates):
    result_next = list_next_risk[:level] + [np.min([list_next_risk[level], list_next_risk[level + 2]])] + list_next_risk[level + 3:]
    list_current_risk_down = list(np.array(result_next) + np.array(list_current_updates))
    
    if np.min(np.array(list_current_risk_down) - np.array(list_current_risk)) > 0:
        return list_current_risk, False

    list_current_risk_down = list(np.min(np.concatenate((np.array(list_current_risk_down), np.array(list_current_risk))).reshape([2,-1]), axis=0))
    for item in np.arange(1, level*2):
        list_current_risk_down[item] = np.min([list_current_risk_down[item-1]+list_current_updates[item], list_current_risk_down[item]])
    for item in np.arange(level*2 - 1, -1, -1):
        list_current_risk_down[item] = np.min([list_current_risk_down[item+1]+list_current_updates[item], list_current_risk_down[item]])
    return list_current_risk_down, True

list_risk = [[0]]
list_updates = [[0]]
for level in np.arange(1, list_points.shape[0]):
    print(f'level -> {level}')
    list_updates.append(list(list_points[level,0:level+1] ) + list(list_points[0:level,level][::-1]))
    list_risk.append(list(list_points[level,0:level+1] ) + list(list_points[0:level,level][::-1]))
    result_previous = list_risk[-2][:level] + [list_risk[-2][level - 1] + 10] +  list_risk[-2][level - 1:]
    list_risk[-1] = list(np.array(result_previous) + np.array(list_updates[-1]))
    list_risk[-1] = calculate_risk_up(level, list_risk[-1], list_updates[-1])
    
    deep = 0

    list_risk[-2], change = calculate_risk_down(level - 1, list_risk[-2], list_risk[-1], list_updates[-2])

    if change:
        result_previous = list_risk[-2][:level] + [list_risk[-2][level - 1] + 10] +  list_risk[-2][level - 1:]
        list_risk[-1] = list(np.array(result_previous) + np.array(list_updates[-1]))
        list_risk[-1] = calculate_risk_up(level, list_risk[-1], list_updates[-1])






print(list_risk[-1][level])
print( time.time() - start_time)