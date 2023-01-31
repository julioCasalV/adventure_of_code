import numpy as np
import time
import itertools as it

list_total_beacon = np.loadtxt('input.txt', delimiter = ',', comments='--')
list_scanner = np.loadtxt('input.txt', delimiter = 'hhhh', dtype='str')
list_scanner = [row for row, scanner in enumerate(list_scanner) if scanner[0:3] == "---"]
num_scanner = len(list_scanner)
num_beacon = len(list_total_beacon)
list_beacon = [list_total_beacon[list_scanner[item]-item:list_scanner[item+1]-(item+1)] for item in range(num_scanner-1)]
list_beacon.append(list_total_beacon[list_scanner[-1]-(num_scanner-1):])


def rotations_matrix():
    matrix_change_orig = np.identity(3)
    matrix_change_rotation_x = np.array([[1,0,0],[0,0,1],[0,-1,0]])
    matrix_change_rotation_y_n = np.array([[0,0,-1],[0,1,0],[1,0,0]])
    matrix_change_rotation_y_p = np.array([[0,0,1],[0,1,0],[-1,0,0]])
    matrix_change_rotation_z = np.array([[0,1,0],[-1,0,0],[0,0,1]])
    matrix_rotation = matrix_change_orig
    results = []
    for rotation in range(4):
        matrix_rotation = np.matmul(matrix_rotation,matrix_change_rotation_z)
        matrix_result_item_x = matrix_rotation.copy()
        for orientation in range(4):
            matrix_result_item_x = np.matmul(matrix_result_item_x,matrix_change_rotation_x)
            results.append(matrix_result_item_x)
        matrix_result_item_y = np.matmul(matrix_rotation,matrix_change_rotation_y_n)
        results.append(matrix_result_item_y)
        matrix_result_item_y = np.matmul(matrix_rotation,matrix_change_rotation_y_p)
        results.append(matrix_result_item_y)
    return results

def find_relation(scanner, list_beacon, list_beacon_init_orig, list_beacon_init, list_scanner_coord):
    scanner_matched = False
    list_beacon_final_orig = list_beacon[scanner]
    list_beacon_final = []
    for beacon_ref in list_beacon_final_orig:
        list_beacon_final.append(list_beacon_final_orig - beacon_ref)
    for item_final, list_beacon_final_item in enumerate(list_beacon_final):
        list_beacon_final_item_testing = np.abs(list_beacon_final_item)
        list_beacon_final_item_testing = np.sum(list_beacon_final_item_testing, axis = 1)
        for item_init, list_beacon_init_item in enumerate(list_beacon_init):
            list_beacon_init_item_testing = np.abs(list_beacon_init_item)
            list_beacon_init_item_testing = np.sum(list_beacon_init_item_testing, axis = 1)
            list_same = [beacon_final for beacon_final in list_beacon_final_item_testing if beacon_final in list_beacon_init_item_testing]
            if len(list_same) < 12:
                continue
            for rotation in list_rotations:
                list_same = []
                diff_coord = list_beacon_init_orig[item_init] - np.matmul(list_beacon_final_orig[item_final], rotation)
                list_beacon_final_change_coord = np.matmul(list_beacon_final_orig, rotation) + diff_coord
                for beacon_final in list_beacon_final_change_coord:
                    for beacon_init in list_beacon_init_orig:
                        if (beacon_final == beacon_init).all():
                            list_same.append(beacon_final)
                if len(list_same) >= 12:
                    scanner_matched = True
                    list_beacon[scanner] = list_beacon_final_change_coord
                    list_scanner_coord.append(diff_coord)
                    print(f'diff_coord -> {diff_coord}')
                    print(f'item_init -> {item_init}')
                    print(f'item_final -> {item_final}')
                    return list_beacon, scanner_matched, list_scanner_coord
    return list_beacon, scanner_matched, list_scanner_coord


list_rotations = rotations_matrix()
list_scanner_not_parsed = list(range(num_scanner))
list_scanner_matched = []
scanner_init = 0
list_scanner_not_parsed.remove(scanner_init)
list_scanner_matched.append(scanner_init)

    

#while len(scanner_matched) > 1:
list_scanner_coord = [np.array([0, 0, 0])]
for item in range(30):
    print("item")
    scanner_orig = list_scanner_matched[0]
    list_beacon_init_orig = list_beacon[scanner_orig]
    list_beacon_init = []
    for beacon_ref in list_beacon_init_orig:
        list_beacon_init.append(list_beacon_init_orig - beacon_ref)
    list_scanner_not_parsed_tmp = list_scanner_not_parsed.copy()
    for scanner in list_scanner_not_parsed_tmp:
        print(scanner)
        list_beacon, scanner_matched, list_scanner_coord = find_relation(scanner, list_beacon, list_beacon_init_orig, list_beacon_init, list_scanner_coord)
        if scanner_matched == True:
            list_scanner_matched.append(scanner)
            list_scanner_not_parsed.remove(scanner)
    print(list_scanner_matched)
    list_scanner_matched.remove(scanner_orig)
    if len(list_scanner_not_parsed) == 0:
        break


final_list = []
for beacons in list_beacon:
    for beacon in beacons:
        must_sum = True
        for beacon_final in final_list:
            if (beacon == beacon_final).all():
                must_sum = False
                break
        if must_sum:
            final_list.append(beacon)

max_distance = 0
for list_scanner_init in list_scanner_coord:
    for list_scanner_final in list_scanner_coord:
        distance = np.sum(np.abs(list_scanner_final - list_scanner_init))
        if max_distance < distance:
            max_distance = distance
print(len(final_list))
print(max_distance)