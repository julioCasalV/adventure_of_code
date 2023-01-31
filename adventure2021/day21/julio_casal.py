import numpy as np
import itertools as it

data = np.loadtxt('input.txt', dtype='str')
positions = np.array(data[:,4].astype(int))
score = np.array([0, 0])
die = 0
throws = 0
limit_sup = 21
while max(score) < limit_sup:
    for item, position in enumerate(positions):
        for rolls in range(3):
            die = die + 1
            positions[item] = positions[item] + die
            throws = throws + 1
        positions[item] = positions[item] % 10
        score[item] = score[item] + (10 if positions[item] == 0 else positions[item])
        if score[item] >= limit_sup:
            break
    die = die % 10
print(min(score)*throws)

list_comb = []
for item in list(it.combinations_with_replacement([1 ,2 ,3], 3)):
    list_comb.extend(list(it.permutations(item, 3)))
posibles_throws = np.unique(list_comb, axis = 0)
die_sums, die_counts = np.unique(posibles_throws.sum(axis=1), return_counts=True)


def calc_combinations(position):
    limit_sup = 21
    score = [0]
    positions = [position]
    counts = [1]
    dict_player = {}
    throw = 0
    while len(score) > 0:
        throw = throw + 1
        score_new = []
        counts_new = []
        score_next = []
        counts_next = []
        positions_next = []
        for position_item, score_item, count_item in zip(positions, score, counts):
            for die, count in zip(die_sums, die_counts):
                positions_result = (position_item + die) % 10
                score_result = score_item + (10 if positions_result == 0 else positions_result)
                count_result = count_item * count
                if score_result < limit_sup:
                    score_next.append(score_result)
                    counts_next.append(count_result)
                    positions_next.append(positions_result)
                score_new.append(int(score_result >= limit_sup))
                counts_new.append(count_result)
        dict_player[throw] = {"score": score_new, "counts": counts_new}
        score = score_next
        positions = positions_next
        counts = counts_next
    return dict_player

dict_player_1 = calc_combinations(10)
dict_player_2 = calc_combinations(1)

win = 0
loss = 0
for throw in np.arange(2, min(max(dict_player_1), max(dict_player_2))+1):
    product_player_1_win = sum(np.multiply(dict_player_1[throw]['score'], dict_player_1[throw]['counts']))
    score_loss = [abs(item -1) for item in dict_player_1[throw]['score']]
    product_player_1_loss = sum(np.multiply(score_loss, dict_player_1[throw]['counts']))
    product_player_2_win = sum(np.multiply(dict_player_2[throw]['score'], dict_player_2[throw]['counts']))
    score_loss = [abs(item -1) for item in dict_player_2[throw-1]['score']]
    product_player_2_loss = sum(np.multiply(score_loss, dict_player_2[throw-1]['counts']))
    win = win + product_player_1_win * product_player_2_loss
    loss = loss + product_player_2_win * product_player_1_loss

print(max(win, loss))