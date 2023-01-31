import math
import numpy as np
from datetime import datetime


data = np.loadtxt('input.txt', dtype='str', delimiter="!")
dict_instructions = []
dict_coord = {"x" : 0, "y" : 1, "z" : 2, "w" : 3}
for i, item in enumerate(data):
    if "inp" in item :
        instruction_num = len(dict_instructions)
        dict_instructions.append([])
    dict_instructions[instruction_num].append(item.split(" "))

def calc_instructions(dict_instructions_item, item, result):
    list_results = [0, 0, result, 0]
    for instruction_list in dict_instructions_item:
        variable_princ = dict_coord[instruction_list[1]]
        if len(instruction_list) == 3:
            if instruction_list[2] in dict_coord:
                variable_sec = list_results[dict_coord[instruction_list[2]]]
            else:
                variable_sec = int(instruction_list[2])
        if instruction_list[0] == "inp":
            list_results[variable_princ] = item
        elif instruction_list[0] == "add":
            list_results[variable_princ] = list_results[variable_princ] + variable_sec
        elif instruction_list[0] == "eql":
            list_results[variable_princ] = int(list_results[variable_princ] == variable_sec)
        elif instruction_list[0] == "mul":
            list_results[variable_princ] = list_results[variable_princ] * variable_sec
        elif instruction_list[0] == "div":
            list_results[variable_princ] = math.floor(list_results[variable_princ] / variable_sec)
        elif instruction_list[0] == "mod":
            list_results[variable_princ] = list_results[variable_princ] % variable_sec
        else:
            print("ERROR")
    return list_results


def execute_instructions(dict_instructions, list_pos_numbers):
    list_total_results_up = [(0, 0)]
    for item_instr in range(len(dict_instructions)):
        initial_time = datetime.now()
        print(f"                        ITEM ITERATION - {item_instr}")
        list_total_results = []
        list_total_values = []
        count = 0
        for num_gen, list_total_results_up_item in list_total_results_up:
            for item in list_pos_numbers:
                count = count + 1
                list_results = calc_instructions(dict_instructions[item_instr], item, list_total_results_up_item)
                list_total_values.append(list_results[2])
                list_total_results.append((num_gen*10 + list_results[3], list_results[2]))
                if item_instr == 13 and list_results[2] == 0:
                    print("              RESULT!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    print((num_gen*10 + list_results[3], list_results[2]))
                    return list_total_results
                if count % 2000000 == 1:
                    init_itm = datetime.now()
                    numbers, index = np.unique(list_total_values, return_index=True)
                    index.sort()
                    list_total_values = [list_total_values[item_final] for item_final in index]
                    list_total_results = [list_total_results[item_final] for item_final in index]
                    print(f"UNIQUE - {datetime.now() - init_itm}")
        init_itm = datetime.now()
        numbers, index = np.unique(list_total_values, return_index=True)
        index.sort()
        list_total_results_up = [list_total_results[item_final] for item_final in index]
        print(f"UNIQUE - {datetime.now() - init_itm}")
        print(f"LEN - {len(list_total_results_up)}")
        print(f"MAX - {max(list_total_values)}")
        print(f"TIME - {datetime.now() - initial_time}")
    return list_total_results_up

result = execute_instructions(dict_instructions, [9, 8, 7, 6, 5, 4, 3, 2, 1])
result = execute_instructions(dict_instructions, [1, 2, 3, 4, 5, 6, 7, 8, 9])