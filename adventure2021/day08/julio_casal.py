
import numpy as np
import itertools


data = []#np.genfromtxt('input.txt', delimiter='|')

with open('input.txt') as f:
    for i, line in enumerate(f):
        num_string = line.split(" | ")
        num_string = num_string[1].split()
        data.append(num_string)
print(data)

data_array = np.array(data)

parse_num_sp = lambda t: 1 if len(t) <= 4 or len(t) == 7 else 0

data_ones = np.vectorize(parse_num_sp)(data_array)
print(sum(sum(data_ones)))

data = []#np.genfromtxt('input.txt', delimiter='|')
data_total = []
with open('input.txt') as f:
    for i, line in enumerate(f):
        num_string = line.split(" | ")
        num_string0 = num_string[0].split()
        num_string1 = num_string[1].split()
        data_total.append(num_string0 + num_string1)
        data.append(num_string1)


list_combinations_bruta = list(itertools.permutations("abcdefg"))
list_combinations = []
for item in list_combinations_bruta:
    num_zero = "".join(sorted([item[0], item[1], item[2], item[4], item[5], item[6]]))
    num_one = "".join(sorted([item[2], item[5]]))
    num_two = "".join(sorted([item[0], item[2], item[3], item[4], item[6]]))
    num_three = "".join(sorted([item[0], item[2], item[3], item[5], item[6]]))
    num_four = "".join(sorted([item[1], item[2], item[3], item[5]]))
    num_five = "".join(sorted([item[0], item[1], item[3], item[5], item[6]]))
    num_six = "".join(sorted([item[0], item[1], item[3], item[4], item[5], item[6]]))
    num_seven = "".join(sorted([item[0],  item[2], item[5]]))
    num_eigth = "".join(sorted([item[0], item[1], item[2], item[3], item[4], item[5], item[6]]))
    num_nine = "".join(sorted([item[0], item[1], item[2], item[3], item[5], item[6]]))
    list_combinations.append([num_zero, num_one , num_two , num_three, num_four, num_five, num_six , num_seven, num_eigth, num_nine])


total = 0
for list_total, list_final in zip(data_total, data):
    list_combinations_item = list_combinations
    for word in list_total:
        word_sort = "".join(sorted(list(word)))
        list_combinations_item = [item for item in list_combinations_item if word_sort in item]
        dict_combination = dict(zip(list_combinations_item[0], list(range(10))))
    num_traducted = ""
    for word_result in list_final:
        word_sort = "".join(sorted(list(word_result)))
        num_traducted += str(dict_combination[word_sort])
    total += int(num_traducted)
print(total)