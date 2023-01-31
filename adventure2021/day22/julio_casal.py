from xmlrpc.client import boolean
import numpy as np
import itertools as it
import pandas as pd

data = np.loadtxt('input.txt', dtype='str')

def parse_coord(coord):
    coord = coord.split("=")[1]
    return [int(i) for i in coord.split("..")]

dict_turns = {}
list_turns = []
list_x1 = []
list_x2 = []
list_y1 = []
list_y2 = []
list_z1 = []
list_z2 = []
max_coord = 0
for i, item in enumerate(data):
    coord = item[1].split(",")
    turn = 1 if item[0] == 'on' else 0
    dict_turns[i] = {"turn" : turn, "x" : parse_coord(coord[0]), "y":parse_coord(coord[1]), "z":parse_coord(coord[2])}
    list_turns.append(turn)
    list_x1.append(parse_coord(coord[0])[0])
    list_x2.append(parse_coord(coord[0])[1])
    list_y1.append(parse_coord(coord[1])[0])
    list_y2.append(parse_coord(coord[1])[1])
    list_z1.append(parse_coord(coord[2])[0])
    list_z2.append(parse_coord(coord[2])[1])
matrix = {}
max_coord = 50
df = pd.DataFrame({"turn" : list_turns, "x1":list_x1, "x2":list_x2, "y1":list_y1, "y2":list_y2, "z1":list_z1, "z2":list_z2})

for i in range(2):
    matrix = np.zeros((max_coord*2, max_coord*2, max_coord*2), dtype='uint8')


for item in dict_turns:
    x = dict_turns[item]["x"] 
    y = dict_turns[item]["y"] 
    z = dict_turns[item]["z"] 
    x = [coord + max_coord for coord in x]
    y = [coord + max_coord for coord in y]
    z = [coord + max_coord for coord in z]
    matrix[x[0]:x[1]+1, y[0]:y[1]+1, z[0]:z[1]+1] = dict_turns[item]["turn"]


x_coord = []
y_coord = []
z_coord = []

def calc_sizes(x_coord, sides):
    side_x = []
    for x, _ in enumerate(x_coord):
        if x_coord[x] >= sides[0] and x_coord[x] <= sides[1]:
            side_x.append([x_coord[x], x_coord[x]])
        if x < (len(x_coord) -1) and x_coord[x]+1 >= x_coord[x]-1:
            if x_coord[x+1]-1 >= sides[0] and x_coord[x]+1 <= sides[1]:
                side_x.append([x_coord[x]+1, x_coord[x+1]-1])
    return side_x

def square_in(original, compare):
    if original["x"][0] <= compare["x"][1] and original["x"][1] >= compare["x"][0] and \
                    original["y"][0] <= compare["y"][1] and original["y"][1] >= compare["y"][0] and \
                        original["z"][0] <= compare["z"][1] and original["z"][1] >= compare["z"][0]:
                        return True
    return False

def square_total_in(original, compare):
    if original["x"][0] <= compare[0][1] and original["x"][1] >= compare[0][0] and \
                    original["y"][0] <= compare[1][1] and original["y"][1] >= compare[1][0] and \
                        original["z"][0] <= compare[2][1] and original["z"][1] >= compare[2][0]:
                        return True
    return False

def square_total_into(original, compare):
    if original[0][0] <= compare[0][0] and original[0][1] >= compare[0][1] and \
                    original[1][0] <= compare[1][0] and original[1][1] >= compare[1][1] and \
                        original[2][0] <= compare[2][0] and original[2][1] >= compare[2][1]:
                        return True
    return False

list_relations = []
for item in dict_turns:
    dict_turns[item]["squares"] = []
    for square in dict_turns:
        if item != square and square_in(dict_turns[item], dict_turns[square]):
                dict_turns[item]["squares"].append(square)
    list_relations.append(dict_turns[item]["squares"])
df["relations"] = list_relations
print(df)

def calc_square_join(list_squares):
    result = 0
    coord_x = [-1000000000, 100000000000000]
    coord_y = [-1000000000, 100000000000000]
    coord_z = [-1000000000, 100000000000000]
    for square in list_squares:
        if dict_turns[square]["x"][0] > coord_x[0]:
            coord_x[0] = dict_turns[square]["x"][0]
        if dict_turns[square]["y"][0] > coord_y[0]:
            coord_y[0] = dict_turns[square]["y"][0]
        if dict_turns[square]["z"][0] > coord_z[0]:
            coord_z[0] = dict_turns[square]["z"][0]
        if dict_turns[square]["x"][1] < coord_x[1]:
            coord_x[1] = dict_turns[square]["x"][1]
        if dict_turns[square]["y"][1] < coord_y[1]:
            coord_y[1] = dict_turns[square]["y"][1]
        if dict_turns[square]["z"][1] < coord_z[1]:
            coord_z[1] = dict_turns[square]["z"][1]
    if coord_x[0] <= coord_x[1] and coord_y[0] <= coord_y[1] and coord_z[0] <= coord_z[1]:
        result = (coord_x[1]-coord_x[0]+1)*(coord_y[1]-coord_y[0]+1)*(coord_z[1]-coord_z[0]+1)
    return result

def calc_square_join_df(list_squares):
    result = 0
    list_squares = list(list_squares)
    inf_coord = df.loc[list_squares, ["x1", "y1", "z1"]].max().reset_index()
    sup_coord = df.loc[list_squares, ["x2", "y2", "z2"]].min().reset_index()
    result_sides = sup_coord[0]-inf_coord[0]
    if result_sides.min() >= 0:
        result = (result_sides[0] + 1) * (result_sides[1] + 1) * (result_sides[2] + 1)
    return result

print(calc_square_join_df(tuple([0, 1, 2])))

list_relations = []
list_values = []

for square in dict_turns:
    list_countinue_relation = dict_turns[square]["squares"]
    for item in range(90):
        relations_tmp = list(it.combinations(list_countinue_relation, item))
        relations_tmp = [item1 + (square,) for item1 in relations_tmp]
        relations_tmp = [tuple(sorted(item1)) for item1 in relations_tmp]
        list_countinue_relation_tmp = []
        for relation in relations_tmp:
            result_join = calc_square_join(relation)
            if result_join > 0:
                list_countinue_relation_tmp.extend(relation)
                list_relations.append(relation)
                list_values.append(result_join)
        if len(list_countinue_relation_tmp) == 0:
            break

list_relations, index = np.unique(list_relations, return_index=True)
list_values = np.array([list_values[item] for item in index])

max_joins = max([len(item) for item in list_relations])
dict_joins = {}

print("medio")
total_sum = 0
for num_joins in list(np.arange(1, max_joins+1))[::-1]:
    index = [i for i, item in enumerate(list_relations) if len(item) == num_joins]
    relations_tmp = list_relations[index]
    values_tmp = list_values[index]
    turn_tmp = [dict_turns[max(item)]["turn"] for item in relations_tmp]
    dict_joins[num_joins] = {}
    for item in range(len(turn_tmp)):
        dict_joins[num_joins][relations_tmp[item]] = {"turn" : turn_tmp[item], "value" : values_tmp[item]}
        if num_joins != max_joins:
            for i_sup in np.arange(num_joins+1,  max_joins+1):
                for item_sup_join in dict_joins[i_sup]:
                    if set(relations_tmp[item]).issubset(item_sup_join):
                        dict_joins[num_joins][relations_tmp[item]]["value"] = dict_joins[num_joins][relations_tmp[item]]["value"] - dict_joins[i_sup][item_sup_join]["value"]
        total_sum = total_sum + dict_joins[num_joins][relations_tmp[item]]["value"]*dict_joins[num_joins][relations_tmp[item]]["turn"]


print(total_sum)
