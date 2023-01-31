
import numpy as np 
data_list = []
with open('input.txt') as f:
    for i, line in enumerate(f):
        data_list.append(np.array(list(line.split()[0])))

dicctionary_chars = {"[":"]", "{":"}", "(":")", "<":">"}
dicctionary_chars_num = {"]":57, "}":1197, ")":3, ">":25137}
dicctionary_chars_point = {"]":2, "}":3, ")":1, ">":4}


total = 0
for line in data_list:
    char_list = []
    for char in line:
        if char in ["[", "{", "(", "<"]:
            char_list.append(dicctionary_chars[char])
        else :
            if char_list[-1] == char:
                char_list = char_list[0:-1] 
            else:
                total += dicctionary_chars_num[char]
                break

print(total)


score_list = []
for line in data_list:
    char_list = []
    corrupted = False
    for char in line:
        if char in ["[", "{", "(", "<"]:
            char_list.append(dicctionary_chars[char])
        else :
            if char_list[-1] == char:
                char_list = char_list[0:-1] 
            else:
                total += dicctionary_chars_num[char]
                corrupted = True
                break
    if corrupted == False:
        score = 0
        for char in reversed(char_list):
            score *= 5
            score += dicctionary_chars_point[char]
        score_list.append(score)

print(np.median(score_list))