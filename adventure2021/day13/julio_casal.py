import numpy as np
from matplotlib import pyplot as plt

list_points = np.loadtxt('input.txt', delimiter = ",", comments='fold')
list_folds = np.loadtxt('input.txt', delimiter = "=", skiprows=list_points.shape[0], dtype='str')
list_folds[:,0] = np.vectorize(lambda x : 0 if x == 'fold along x' else 1)(list_folds[:,0])
list_folds = list_folds.astype(int)

def fold(side, row, points):
    points[:,side] = np.vectorize(lambda x : x if x < row else 2*row - x )(points[:,side])
    points = np.unique(points, axis=0)
    return points

for [side, row] in list_folds:
    list_points = fold(side, row, list_points)
    print(list_points.shape)
list_points = list_points.astype(int)

result = np.zeros((np.max(list_points[:,0])+1, np.max(list_points[:,1])+1))

for [x, y] in list_points.astype(int):
    result[x, y] = 1

plt.imshow(result.T, interpolation='nearest')
plt.show()