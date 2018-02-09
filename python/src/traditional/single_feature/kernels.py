import numpy as np
from scipy.spatial.distance import *
from sklearn.metrics.pairwise import *
from scipy.stats import spearmanr, kendalltau
from sklearn.metrics.pairwise import *

import gc
from scipy.spatial.distance import chebyshev


def linear_kernel(matrix_1, matrix_2):
    cos = paired_cosine_distances(matrix_1, matrix_2)
    man = paired_manhattan_distances(matrix_1, matrix_2)
    euc = paired_euclidean_distances(matrix_1, matrix_2)
    che = []
    for row_1, row_2 in zip(matrix_1, matrix_2):
        che.append(chebyshev(row_1, row_2))
    che = np.asarray(che)
    out = np.vstack((cos, man, euc, che)).T
    return out


from scipy.stats import pearsonr, spearmanr, kendalltau


def stat_kernel(matrix_1, matrix_2):
    pearson = []
    spearman = []
    kendall = []
    for row_1, row_2 in zip(matrix_1, matrix_2):
        pearson.append(pearsonr(row_1, row_2)[0])
        spearman.append(spearmanr(row_1, row_2)[0])
        kendall.append(kendalltau(row_1, row_2)[0])
    out = np.vstack((pearson, spearman, kendall)).T
    return out


def non_linear_kernel(matrix_1, matrix_2):
    polynomial = []
    rbf = []
    laplacian = []
    sigmoid = []
    for row_1, row_2 in zip(matrix_1, matrix_2):
        row_1 = row_1.reshape(len(row_1), 1).T
        row_2 = row_2.reshape(len(row_2), 1).T
        polynomial.append(polynomial_kernel(row_1, row_2)[0][0])
        rbf.append(rbf_kernel(row_1, row_2)[0][0])
        laplacian.append(laplacian_kernel(row_1, row_2)[0][0])
        sigmoid.append(sigmoid_kernel(row_1, row_2)[0][0])
    out = np.vstack((polynomial, rbf, laplacian, sigmoid)).T
    return out


if __name__ == '__main__':
    a = np.asarray([[1, 2, 3], [2, 4, 6], [3, 4, 5]])
    b = np.asarray([[2, 4, 6], [3, 4, 5], [4, 5, 6]])
    # c = linear_kernel(a, b)
    # d = non_linear_kernel(a, b)
    e = stat_kernel(a, b)
    print(e)
