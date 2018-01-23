from nltk import ChartParser
from nltk.tokenize import word_tokenize
import math
import numpy as np

# tuning param. indicating the importance of the size factor
lmda = 2
# tuning param. indicating the importance of the depth factor
mu = 1.5

# Matrix storing similarity score, for the purpose of dynamic programming
matrix = np.empty([1, 1])


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

# TODO
def get_matched_tree_fragments(tree_fragment_1, tree_fragment_2):
    """
    get all matched tree fragments

    :param tree_fragment_1:
    :param tree_fragment_2:
    :return:
    """
    re = []

    # TODO: Two nested loops is not necessary, there is a faster algorithm to implement this
    for subtree_1 in tree_fragment_1.subtrees():
        for subtree_2 in tree_fragment_2.subtrees():
            if subtree_1 == subtree_2:
                re.append((subtree_1, subtree_2))
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

    # TODO: node1 == node2 means the production rule and the label are both the same, need to rewrite equal method
    if node1.is_terminal is True and node2.is_terminal is True:
        score = delta1 * delta2 * \
                math.pow(lmda, s1 + s2) * \
                math.pow(mu, d1 + d2)
        matrix[node1.index, node2.index] = score
        return score
    else:
        # len(node.children_list) is not size of node
        prefix = math.pow(delta1, eta) * math.pow(delta2, eta) * math.pow(lmda, 2 * eta) * \
                 math.pow(mu, eta * (2 - (1 + len(node1.children_list)) * (d1 + d2)))
        for j in range(len(node1.children_list)):
            child1 = node1.children_list[j]
            child2 = node2.children_list[j]
            if matrix[child1.index, child2.index] is not np.nan:
                score *= matrix[child1.index, child2.index]
            else:
                score *= node_matching_score(node1.children_list[j], node2.children_list[j])
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
    # To apply dynamic programming, we should add child index inside a syntactic tree -> Done!
    # Initialize similarity matrix
    global matrix
    matrix = np.empty([tree1.size, tree2.size])
    matrix.fill(np.nan)

    descendants1 = tree1.subtrees()
    descendants2 = tree2.subtrees()
    score = 0

    for node1 in descendants1:
        for node2 in descendants2:
            # To match index, remember to set root index as 0 -> Done!

            if np.isnan(matrix[node1.index, node2.index]):
                score += node_matching_score(node1, node2)
            else:
                score += matrix[node1.index, node2.index]
    return score


def normalized_simialrity_score(tree1, tree2):
    """
    Normalized similarity score betweeen two trees

    :param tree1:
    :param tree2:
    :return:
    """
    return similarity_score(tree1, tree2) / math.sqrt(similarity_score(tree1, tree1) * similarity_score(tree2, tree2))


# TODO
def get_syntactic_prase_tree(sentence):
    """

    :param sentence:
    :return:
    """
    tokened_sentence = word_tokenize(sentence)


if __name__ == '__main__':
    sentence1 = '(ROOT (S (NP (PRP It)) (VP (VBZ is) (ADJP (RB so) (JJ good))) (. .)))'
    sentence2 = '(ROOT (S (NP (PRP It)) (VP (VBZ is) (ADJP (RB so) (JJ bad))) (. .)))'
    from python.src.traditional.pair_feature.structure.node import Node

    n1 = Node.fromstring(sentence1)
    n2 = Node.fromstring(sentence2)
    n1.update_tree()
    n2.update_tree()

    common = get_matched_tree_fragments(n1, n2)
    score1 = similarity_score(n1, n2)
    print("Hello World!")
