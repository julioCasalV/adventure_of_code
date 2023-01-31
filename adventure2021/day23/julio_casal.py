import numpy as np

data = np.loadtxt('input.txt', dtype='str', comments="!")
print(data)


def add_play(dict_plays_new, list_plays_new, way, list_house, list_amph, result):
    play = ("".join([str(int(item)) for item in (list_amph + way.tolist())]))
    exist_entrie = np.where(list_plays_new == play)[0]
    if len(exist_entrie) == 0:
        list_plays_new = np.append(list_plays_new, play)
        dict_plays_new.append({"result": result, "way": way, "house": list_house, "list_amph": list_amph})
    else:
        if dict_plays_new[exist_entrie[0]]["result"] > result:
            dict_plays_new[exist_entrie[0]]["result"] = result
    return dict_plays_new, list_plays_new

def check_initial_conditions(house, list_amph):
    for amph in list_amph[::-1]:
        result = True
        x, y = np.where(house == amph)
        print((house.shape[1]))
        for item in np.arange(y[0], house.shape[1]):
            if x[0] != dict_amph[house[x[0], item]]["house"]:
                result = False
        if result == True:
            list_amph.remove(amph)
    return list_amph

def can_go_out(amph, house):
    x, y = np.where(house == amph)
    if y[0] > 0 and (house[x[0], 0 : y[0]] > 0).any():
        return 0, 0, False
    return x[0], y[0], True

def calc_stop_zones(way, house_zone):
    posibl_stop = np.where(way > 0)[0]
    list_stops = np.where(posibl_stop < house_zone)[0]
    if list_stops.shape[0] == 0:
        inf_step = -1
    else:
        inf_step = posibl_stop[list_stops[-1]]
    list_stops = np.where(posibl_stop > house_zone)[0]
    if list_stops.shape[0] == 0:
        sup_step = 11
    else:
        sup_step = posibl_stop[list_stops[0]]
    step_to_stop = [item for item in stop_zones if item > inf_step and item < sup_step]
    return step_to_stop

def calc_possible_moves(amph, way, house, result_orig, list_amph, dict_plays_new, list_plays_new, result_total):
    result_final = 1000000000000000000000
    into_amph = False
    if amph not in way:
        x, y, evaluate = can_go_out(amph, house)
        if evaluate == False:
            return dict_plays_new, list_plays_new, into_amph, result_final
        house_zone = house_zones[x]
        house[x, y] = 0
        step_to_stop = calc_stop_zones(way, house_zone)
        for item in step_to_stop:
            way_mod = way.copy()
            way_mod[item] = amph
            result = (abs(item-house_zone) + 1 + y) * dict_amph[amph]["weight"] + result_orig
            if result < result_total:
                dict_plays_new, list_plays_new = add_play(dict_plays_new, list_plays_new, way_mod, house, list_amph, result)
    else:
        amph_house = dict_amph[amph]["house"]
        x = np.where(way == amph)[0][0]
        way_item = way[min(x, house_zones[amph_house])+1 : max(x, house_zones[amph_house])]
        house_pos = sum(house[amph_house, :] == 0)
        coincid = (np.remainder(house[amph_house, house_pos:] - 1, 4) == (amph-1)%4).all()
        if house_pos > 0 and \
            (house_pos == house.shape[1] or coincid) and \
            (way_item.shape[0] == 0 or way_item.max() == 0):
            into_amph = True
            way[x] = 0
            result = (way_item.shape[0] + 1 + house_pos) * dict_amph[amph]["weight"] + result_orig
            if result < result_total:
                list_amph.remove(amph)
                house[amph_house, house_pos - 1] = amph
                dict_plays_new, list_plays_new = add_play(dict_plays_new, list_plays_new, way, house, list_amph, result)
                if len(list_amph) == 0:
                    result_final = result
    return dict_plays_new, list_plays_new, into_amph, result_final

list_house = np.array([[5, 1], [6, 2], [8, 3], [4, 7]])
list_house = np.array([[2, 1], [3, 4], [6, 7], [8, 5]])
list_house = np.array([[2, 12, 1], [3, 11, 4], [6, 14, 7], [8, 13, 5]])
list_house = np.array([[2, 12, 16, 1], [3, 11, 10, 4], [6, 14, 9, 7], [8, 13, 15, 5]])
#list_house = np.array([[2, 3], [6, 7], [4, 1], [8, 5]])
list_house = np.array([[2, 12, 16, 3], [6, 11, 10, 7], [4, 14, 9, 1], [8, 13, 15, 5]])
way = np.zeros(11)

house_zones = [2, 4, 6, 8]
stop_zones = [0, 1, 3, 5, 7, 9, 10]
list_amph = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
dict_amph = {1: {"weight": 1, "house": 0, "step": 4}, 2: {"weight": 10, "house": 1, "step": 6}, 
            3: {"weight": 100, "house": 2, "step": 8}, 4: {"weight": 1000, "house": 3, "step": 10},
            5: {"weight": 1, "house": 0, "step": 4}, 6: {"weight": 10, "house": 1, "step": 6}, 
            7: {"weight": 100, "house": 2, "step": 8}, 8: {"weight": 1000, "house": 3, "step": 10},
            9: {"weight": 1, "house": 0, "step": 4}, 10: {"weight": 10, "house": 1, "step": 6}, 
            11: {"weight": 100, "house": 2, "step": 8}, 12: {"weight": 1000, "house": 3, "step": 10},
            13: {"weight": 1, "house": 0, "step": 4}, 14: {"weight": 10, "house": 1, "step": 6}, 
            15: {"weight": 100, "house": 2, "step": 8}, 16: {"weight": 1000, "house": 3, "step": 10},
            0: {"weight": 0, "house": 0, "step": 0}}


list_amph = check_initial_conditions(list_house, list_amph)

print(list_amph)
print(int("".join([str(int(item)) for item in (list_amph + way.tolist())])))
dict_plays = [{"result": 0, "way": way, "house": list_house, "list_amph": list_amph}]
print("-------")
result_total = 100000000000000000000000000000000000
caos = 0
while len(dict_plays) > 0 and caos < 40:
    caos = caos + 1
    print(caos)
    dict_plays_new = []
    item = 0
    list_plays_new = np.array([])
    for play in dict_plays:
        prior = np.where(play["way"] > 0)
        list_amphs_to_evaluate = list(play["way"][prior].astype(int)) + [item for item in play["list_amph"] if item not in play["way"][prior]]
        for amph in list_amphs_to_evaluate:
            dict_plays_new, list_plays_new, into_amph, result = calc_possible_moves(amph, play["way"].copy(), play["house"].copy(), 
                                                                play["result"], play["list_amph"].copy(), 
                                                                dict_plays_new, list_plays_new, result_total)
            if result_total > result:
                result_total = result
            if into_amph:
                break
    dict_plays = dict_plays_new.copy()
    #print(list_plays_new)
    #print(dict_plays)
    #print(len(dict_plays_new))
    #print(len(list_plays_new))
    print(f'len(dict_plays) = {len(dict_plays)} result = {result_total}')
    if len(dict_plays) == 0:
        break

print(dict_plays)
print(result_total)


