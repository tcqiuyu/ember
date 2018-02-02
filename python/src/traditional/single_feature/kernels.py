import numpy as np
from scipy.spatial.distance import *
from sklearn.metrics.pairwise import *
from scipy.stats import spearmanr, kendalltau
from sklearn.metrics.pairwise import *


def linear_kernel_vector(features_1, features_2):
    cos = cosine(features_1, features_2)
    man = cityblock(features_1, features_2)
    euc = euclidean(features_1, features_2)
    che = chebyshev(features_1, features_2)

    return {'cosine': cos, 'manhattan': man, 'euclidean': euc, 'chebyshev': che}


def linear_kernel_matrix(matrix_1, matrix_2):
    cos = pairwise_distances(matrix_1, matrix_2, metric='cosine')
    man = pairwise_distances(matrix_1, matrix_2, metric='manhattan')
    euc = pairwise_distances(matrix_1, matrix_2, metric='euclidean')
    che = pairwise_distances(matrix_1, matrix_2, metric='chebyshev')
    return {'cosine': cos, 'manhattan': man, 'euclidean': euc, 'chebyshev': che}


def stat_kernel(matrix_1, matrix_2):
    cor_matrix = np.corrcoef(matrix_1, matrix_2)
    shp = cor_matrix.shape[0] / 2
    pearson = cor_matrix[:shp, shp:]

    spear_matrix = spearmanr(matrix_1, matrix_2, axis=1)
    spearman = spear_matrix[:shp, shp:]

    kendall = np.zeros(shape=[shp, shp])
    for idx_i, i in enumerate(matrix_1):
        for idx_j, j in enumerate(matrix_2):
            kendall[idx_i, idx_j] = kendalltau(i, j)

    return {'pearson': pearson, 'spearman': spearman, 'kendall': kendall}


def non_linear_kernel(matrix_1, matrix_2):
    polynomial = polynomial_kernel(matrix_1, matrix_2)
    rbf = rbf_kernel(matrix_1, matrix_2)
    laplacian = laplacian_kernel(matrix_1, matrix_2)
    sigmoid = sigmoid_kernel(matrix_1, matrix_2)

    return {'polynomial': polynomial, 'rbf': rbf, 'laplacian': laplacian, 'sigmoid': sigmoid}
