import numpy as np
import time
import re
import math
import itertools as it

list_pairs_string = np.loadtxt('input.txt', dtype='str')

def build_list_pairs_string(list_pairs_string):
    list_pairs_num = []
    list_pairs_level = []
    list_pairs_pos = []
    pos_string = ""
    level = -1

    for item, char in enumerate(list_pairs_string):
        if char == "[":
            level += 1
            pos_string = pos_string + "0"
        elif char == "]":
            level -= 1
            pos_string = pos_string[:-1]
        elif char == ",":
            pos_string = pos_string[:-1] + "1"
        elif re.fullmatch('[0-9]+', char) is not None:
            list_pairs_num.append(int(char))
            list_pairs_level.append(level)
            list_pairs_pos.append(pos_string)
    return list_pairs_num, list_pairs_level, list_pairs_pos

def build_list_pairs(list_pairs_num, list_pairs_level, list_pairs_pos, side):
    for item, char in enumerate(list_pairs_num):
        list_pairs_level[item] = list_pairs_level[item] + 1
        list_pairs_pos[item] = str(side) + list_pairs_pos[item]
    return list_pairs_num, list_pairs_level, list_pairs_pos

def split(list_pairs_num, list_pairs_level, list_pairs_pos, pos):
    ###print(f'{list_pairs_num[:pos]} \033[92m{list_pairs_num[pos]} \033[0m{list_pairs_num[pos+1:]}')
    list_pairs_num.insert(pos+1,math.ceil(list_pairs_num[pos]/2))
    list_pairs_level.insert(pos+1,list_pairs_level[pos]+1)
    list_pairs_pos.insert(pos+1,list_pairs_pos[pos]+'0')
    list_pairs_num[pos] = math.floor(list_pairs_num[pos]/2)
    list_pairs_level[pos] = list_pairs_level[pos] + 1
    list_pairs_pos[pos] = list_pairs_pos[pos] + '1'
    return list_pairs_num, list_pairs_level, list_pairs_pos

def explode(list_pairs_num, list_pairs_level, list_pairs_pos, pos):
    ##print(f'{list_pairs_num[:pos]} \033[92m{list_pairs_num[pos:pos+2]} \033[0m{list_pairs_num[pos+2:]}')
    num_left = list_pairs_num[pos]
    num_rigth = list_pairs_num[pos+1]
    list_pairs_num[pos] = 0
    list_pairs_level[pos] = list_pairs_level[pos] - 1
    list_pairs_pos[pos] = list_pairs_pos[pos][:-1]
    list_pairs_num.pop(pos+1)
    list_pairs_level.pop(pos+1)
    list_pairs_pos.pop(pos+1)
    if pos > 0:
        list_pairs_num[pos-1] = list_pairs_num[pos-1] + num_left
    if pos < len(list_pairs_num) - 1:
        list_pairs_num[pos+1] = list_pairs_num[pos+1] + num_rigth
    return list_pairs_num, list_pairs_level, list_pairs_pos
    
def find_explode(list_pairs_num, list_pairs_level, list_pairs_pos):
    work = False
    for item in range(len(list_pairs_num)-1):
        if list_pairs_level[item] >= 4 and list_pairs_pos[item][:-1] == list_pairs_pos[item+1][:-1]:
            work = True
            list_pairs_num, list_pairs_level, list_pairs_pos = explode(list_pairs_num, list_pairs_level, list_pairs_pos, item)
            break
    return list_pairs_num, list_pairs_level, list_pairs_pos, work

def find_split(list_pairs_num, list_pairs_level, list_pairs_pos):
    work = False
    for item in range(len(list_pairs_num)):
        if list_pairs_num[item] >= 10:
            work = True
            list_pairs_num, list_pairs_level, list_pairs_pos = split(list_pairs_num, list_pairs_level, list_pairs_pos, item)
            break
    return list_pairs_num, list_pairs_level, list_pairs_pos, work

def calc_sum(list_pairs_num, list_pairs_level, list_pairs_pos):
    for i in range(200000):
        work_exp = True
        for i in range(200000):
            list_pairs_num, list_pairs_level, list_pairs_pos, work_exp = find_explode(list_pairs_num, list_pairs_level, list_pairs_pos)
            if work_exp == False:
                break
        list_pairs_num, list_pairs_level, list_pairs_pos, work_spl = find_split(list_pairs_num, list_pairs_level, list_pairs_pos)
        if work_exp == False and work_spl == False:
            break
        #print("---t------------")
        #print(list_pairs_num)
    return list_pairs_num, list_pairs_level, list_pairs_pos

def magnitude(list_pairs_num, list_pairs_level, list_pairs_pos):
    for i in range(200000):
        if len(list_pairs_num) == 1:
            break
        for pos in range(len(list_pairs_num)-1):
            if list_pairs_pos[pos][:-1] == list_pairs_pos[pos+1][:-1]:
                list_pairs_num[pos] = 3*list_pairs_num[pos] + 2*list_pairs_num[pos+1]
                list_pairs_level[pos] = list_pairs_level[pos] - 1
                list_pairs_pos[pos] = list_pairs_pos[pos][:-1]
                list_pairs_num.pop(pos+1)
                list_pairs_level.pop(pos+1)
                list_pairs_pos.pop(pos+1)
                break
    return list_pairs_num[0]
        
magnitude_max = 0
list_pairs_string_comb = list(it.permutations(list_pairs_string, 2))
for list_pairs_string_item in list_pairs_string_comb:
    list_pairs_pos = []
    list_pairs_level = []
    list_pairs_num = []
    for list_pairs in list_pairs_string_item:
        list_pairs_num_item, list_pairs_level_item, list_pairs_pos_item = build_list_pairs_string(list_pairs)
        if len(list_pairs_pos) > 0:
            list_pairs_num, list_pairs_level, list_pairs_pos = build_list_pairs(list_pairs_num, list_pairs_level, list_pairs_pos, 0)
            list_pairs_num_item, list_pairs_level_item, list_pairs_pos_item =  build_list_pairs(list_pairs_num_item, list_pairs_level_item, list_pairs_pos_item, 1)
        list_pairs_num = list_pairs_num + list_pairs_num_item
        list_pairs_level = list_pairs_level + list_pairs_level_item
        list_pairs_pos = list_pairs_pos + list_pairs_pos_item
        list_pairs_num, list_pairs_level, list_pairs_pos = calc_sum(list_pairs_num, list_pairs_level, list_pairs_pos)

    magnitude_item = magnitude(list_pairs_num, list_pairs_level, list_pairs_pos)
    if magnitude_item > magnitude_max:
        magnitude_max = magnitude_item

print(magnitude_max)