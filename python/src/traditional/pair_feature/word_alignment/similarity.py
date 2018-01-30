from .aligner import *
from ..wordnet import get_wordnet_pos
from nltk.corpus import wordnet as wn


def alignment_similarity(alignment_result):
    alignment_index = alignment_result[0]

    # Number of content word
    content_word_number_1 = alignment_result[2][0]
    content_word_number_2 = alignment_result[2][1]
    score = 2 * len(alignment_index) / (content_word_number_1 + content_word_number_2)
    return score


def verb_alignment_similarity(alignment_result, pos):
    aligned_word_1 = list(filter((lambda x: get_wordnet_pos(x[0][1]) == pos), alignment_result[1]))
    aligned_word_2 = list(filter((lambda x: get_wordnet_pos(x[1][1]) == pos), alignment_result[1]))
    verb_word_1 = list(filter((lambda x: get_wordnet_pos(x) == pos), alignment_result[3][0]))
    verb_word_2 = list(filter((lambda x: get_wordnet_pos(x) == pos), alignment_result[3][1]))

    score = (len(aligned_word_1) + len(aligned_word_2)) / (len(verb_word_1) + len(verb_word_2))

    return score
