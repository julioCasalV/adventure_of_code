

import numpy as np
import time


def board_win_loss(board_sort_list, mode=0):
    boards_sort_winner_hor = board_sort_list.max(axis=1).min(axis=1)
    boards_sort_winner_ver = board_sort_list.max(axis=2).min(axis=1)
    board_reshape = boards_sort_winner_ver.shape[0]
    boards_sort_winner = np.array([boards_sort_winner_hor, boards_sort_winner_ver]).reshape([2, board_reshape]).min(axis=0)
    if mode == 0:
        ball_sort_winner = boards_sort_winner.min()
        board_winner_coord = boards_sort_winner.argmin()
    else:
        ball_sort_winner = boards_sort_winner.max()
        board_winner_coord = boards_sort_winner.argmax()
    return ball_sort_winner, board_winner_coord


def map_zeros(ball):
    if ball <= ball_sort_winner:
        return 0
    else:
        return dictionary_inv.get(ball)

list_balls = np.loadtxt('input.txt', max_rows=1, delimiter = ",")
order_balls = list(range(len(list_balls)))
dictionary = dict(zip(list_balls, order_balls))
dictionary_inv = dict(zip(order_balls, list_balls))
    
board_list = np.loadtxt('input.txt', skiprows=1)
board_list = board_list.reshape(-1, board_list.shape[1], board_list.shape[1])
board_sort_list = np.vectorize(dictionary.get)(board_list)


time_init = time.time()
ball_sort_winner, board_winner_coord = board_win_loss(board_sort_list)
winner_ball = dictionary_inv.get(ball_sort_winner)
board_zeros = np.vectorize(map_zeros)(board_sort_list[board_winner_coord,:,:])

result = sum(sum(board_zeros)) * winner_ball
print('result:', result)
print("--- %s seconds ---" % (time.time() - time_init))


time_init = time.time()
ball_sort_winner, board_winner_coord = board_win_loss(board_sort_list, 1)
winner_ball = dictionary_inv.get(ball_sort_winner)
board_zeros = np.vectorize(map_zeros)(board_sort_list[board_winner_coord,:,:])

result = sum(sum(board_zeros)) * winner_ball
print('result:', result)
print("--- %s seconds ---" % (time.time() - time_init))