import numpy as np
input = 'input.txt'

dict_num = {".": 0, ">": 1, "v": 2}
matrix = np.loadtxt(input, dtype = str)

list_array = []
for row in matrix:
    list_array.append([dict_num[item] for item in row])
matrix = np.array(list_array)

num_rows, num_columns = matrix.shape
for iteration in range(1000):
    change = 0
    for row in range(num_rows):
        moved = 0
        occupped = False
        for column in range(num_columns):
            if matrix[row, column] == 1 and matrix[row, (column + 1) % num_columns] == 0 and moved == 0 and (column < num_columns - 1 or occupped == False):
                matrix[row, (column + 1) % num_columns] = 1
                matrix[row, column] = 0
                change = 1
                moved = 1
                if column == 0:
                    occupped = True
            else :
                moved = 0
    for column in range(num_columns):
        moved = 0
        occupped = False
        for row in range(num_rows):
            if matrix[row, column] == 2 and matrix[(row + 1) % num_rows, column] == 0 and moved == 0 and (row < num_rows - 1 or occupped == False):
                matrix[(row + 1) % num_rows, column] = 2
                matrix[row, column] = 0
                change = 1
                moved = 1
                if row == 0:
                    occupped = True
            else :
                moved = 0
    if change == 0:
        print(iteration + 1)
        break