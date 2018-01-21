from nltk import ChartParser
from nltk.tokenize import word_tokenize
import math
import numpy as np

# delta = 1.2 where node i's POS tag is VB/NN
# delta = 1.1 where node i's POS tag is VP/NP
# delta = 1 otherwise
delta = 0

# theta is the production of all delta's for a tree fragment
theta = 0

# tuning param. indicating the importance of the size factor
lmda = 0
# tuning param. indicating the importance of the depth factor
mu = 0

# Matrix storing similarity score, for the purpose of dynamic programming
matrix = np.empty(1, 1)


def tree_weight(tree_fragment):
    """
    tree_weight = theta*lamda^(size)*mu^(depth)
    :param tree_fragment:
    :return:
    """
    return tree_fragment.theta * \
           math.pow(lmda, tree_fragment.size) * \
           math.pow(mu, tree_fragment.depth)


# def matching_tree_score(tree_fragment_1, tree_fragment_2):
#     return tree_weight(tree_fragment_1) * tree_weight(tree_fragment_2)

def get_matched_tree_fragments(tree_fragment_1, tree_fragment_2):
    re = []
    return re


def node_matching_score(node1, node2):
    """
    M(r1,r2) - The multiplication of weights of all matched tree
    fragments under the roots of r1 and r2. (recursive version)

    :param node1:
    :param node2:
    :return:
    """
    score = 0

    matched_tree_fragments = get_matched_tree_fragments(node1, node2)
    eta = len(matched_tree_fragments)
    delta1 = node1.delta
    delta2 = node2.delta
    # Size is all nodes it contains
    s1 = node1.size
    s2 = node2.size
    # Depth is the level the node currently locates in
    d1 = node1.depth
    d2 = node2.depth

    global matrix

    if node1.is_terminal is True and node2.is_terminal is True:
        score = delta1 * delta2 * \
                math.pow(lmda, s1 + s2) * \
                math.pow(mu, d1 + d2)
        matrix[node1.index, node2.index] = score
        return score

    else:
        prefix = math.pow(delta1, eta) * math.pow(delta2, eta) * math.pow(lmda, 2 * eta) * \
                 math.pow(mu,
                          eta * (2 - (1 + len(node1.children)) * (d1 + d2)))  # len(node.children) is not size of node
        for j in range(len(node1.children)):
            child1 = node1.children[j]
            child2 = node2.children[j]
            if matrix[child1.index, child2.index] is not np.nan:
                score *= matrix[child1.index, child2.index]
            else:
                score *= node_matching_score(node1.children[j], node2.children[j])

        score = prefix * score
        matrix[node1.index, node2.index] = score
        return score


def similarity_score(tree1, tree2):
    """
    Using dynamic programming to calculate the similarity between two syntactic trees

    :param tree1:
    :param tree2:
    :return:
    """
    # TODO: To apply dynamic programming, we should add child index inside a syntactic tree
    # Initialize similarity matrix
    global matrix
    matrix = np.empty(tree1.size, tree2.size)
    matrix.fill(np.nan)

    descendants1 = tree1.get_descendants()
    descendants2 = tree2.get_descendants()
    score = 0

    for node1 in descendants1:
        for node2 in descendants2:
            # TODO: to match index, remember to set root index as 0
            if matrix[node1.index, node2.index] is not np.nan:
                score += node_matching_score(node1, node2)
            else:
                score += matrix[node1.index, node2.index]
    return


def get_syntactic_prase_tree(sentence):
    tokened_sentence = word_tokenize(sentence)


def eval_pair_set():
    return


if __name__ == '__main__':
    eval_pair_set()
