import numpy as np

list_points = np.loadtxt('input.txt', max_rows = 1, dtype='str')
list_relations = np.loadtxt('input.txt', delimiter = " -> ", skiprows=1, dtype='str')
list_points = list_points.astype(str)
list_points = np.array_str(list_points)
char_value = np.unique(list_relations[:,1])
relation_value = np.unique(list_relations[:,0])
dict_relations = dict(list_relations)
list_points_sep = list(list_points)

dict_char_counts = dict(zip(char_value, np.zeros(char_value.shape[0])))
for item in list_points_sep:
    dict_char_counts[item] = dict_char_counts[item] + 1

dict_relation_counts_zeros = dict(zip(relation_value, np.zeros(relation_value.shape[0])))
dict_relation_counts = dict_relation_counts_zeros.copy()
for letter_num in range(len(list_points_sep) - 1):
    relation = "".join(list_points_sep[letter_num:letter_num+2])
    dict_relation_counts[relation] = dict_relation_counts[relation] + 1

dict_relations_total = {}
for item in dict_relations:
    dicc_tmp = {"char" : dict_relations[item], "fut_relation" : [item[0] + dict_relations[item], dict_relations[item] + item[1]] }
    dict_relations_total[item] = dicc_tmp


for item in range(40):
    dict_relation_counts_before = dict_relation_counts.copy()
    dict_relation_counts = dict_relation_counts_zeros.copy()
    for relation in dict_relation_counts_before:
        count_relation = dict_relation_counts_before[relation]
        char_add = dict_relations_total[relation]["char"]
        relations_add = dict_relations_total[relation]["fut_relation"]
        dict_char_counts[char_add] = dict_char_counts[char_add] + count_relation
        for fut_relation in relations_add:
            dict_relation_counts[fut_relation] = dict_relation_counts[fut_relation] + count_relation


print(max(dict_char_counts.values()) - min(dict_char_counts.values()))


