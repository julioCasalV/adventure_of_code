import numpy as np
import time

def literal_subpack(text_code):
    keep_reading = "1"
    binary_result = ""
    while keep_reading == "1":
        keep_reading = text_code[0]
        text_code_item = text_code[1:5]
        text_code = text_code[5:]
        binary_result = binary_result + text_code_item
        assert(len(text_code_item)==4)
    result = int(binary_result, 2)
    return text_code, result

def operator(text_code):
    version = text_code[:3]
    int_version = int(version, 2)
    global sum_version
    sum_version = sum_version + int_version
    type = text_code[3:6]
    integer_type = int(type, 2)
    text_code = text_code[6:]
    if integer_type == 4:
        text_code, result = literal_subpack(text_code)
    else:
        length_type = text_code[0]
        if length_type == "0":
            text_code, result = operator_total_length(text_code)
        else:
            text_code, result = operator_num_subpacks(text_code)
        assert(len(result)!=0)
        assert(integer_type != 4 or integer_type <= 7)
        if integer_type == 0:
            result = sum(result)
        elif integer_type == 1:
            result = np.prod(result, dtype='float')
        elif integer_type == 2:
            result = min(result)
        elif integer_type == 3:
            result = max(result)
        elif integer_type == 5:
            result = int(result[0] > result[1])
        elif integer_type == 6:
            result = int(result[0] < result[1])
        elif integer_type == 7:
            result = int(result[0] == result[1])
        
    return text_code, result

def operator_total_length(text_code):
    total_length = text_code[1:16]
    total_length = int(total_length, 2)
    text_code = text_code[16:]
    out_text = len(text_code) - total_length
    result = []
    while len(text_code) > out_text:
        text_code, result_item = operator(text_code)
        result.append(result_item)
    assert(len(text_code)==out_text)
    return text_code, result

def operator_num_subpacks(text_code):
    num_subpacks = text_code[1:12]
    num_subpacks = int(num_subpacks, 2)
    text_code = text_code[12:]
    result = []
    for item in range(num_subpacks):
        text_code, result_item = operator(text_code)
        result.append(result_item)
    return text_code, result

start_time = time.time()

list_hexa = np.loadtxt('input.txt', dtype='str')


hexa = '9C0141080250320F1802104A08'
hexa = str(list_hexa)
integer = int(hexa, 16)
total=len(hexa)*4
text_code = format(integer, f'0>{total}b')
sum_version = 0
text_code, result = operator(text_code)
print(f'\033[92msum_version -> {sum_version} \033[0m')
print(f'\033[92mresult -> {result} \033[0m')