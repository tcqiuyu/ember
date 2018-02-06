import numpy as np

from sklearn.externals import joblib
from traditional.pair_feature import ngram
from traditional.pair_feature import wordnet
from traditional.pair_feature.word_alignment import similarity
from traditional import idf
from preprocessing import corenlp as nlp

import pickle
import logging

training_path_base = "../../../data/training/"

logging.basicConfig(level=logging.INFO,
                    format="%(levelname)s: %(asctime)s %(filename)s[line:%(lineno)d] %(message)s")


def pload(path):
    f = open(path, "rb")
    out = pickle.load(f)
    f.close()
    return out


def pdump(obj, path):
    f = open(path, "wb")
    pickle.dump(obj, f)
    f.close()


# Obtain training data
training_matrix = pload(training_path_base + "training_data.pickle")

sentence_pair_matrix = []
label_matrix = []

# Construct feature matrix
feature_vec = []
feature_matrix = []

# Using Stanford NLP to parsing the sentence pair
lemma_matrix = []
parse_tree_matrix = []  # for syntactic parse features
corpus = []  # for idf
parse_result_matrix = []  # for alignment features


def save_input_matrices(training_matrix):
    for idx, sentence_pair in enumerate(training_matrix):
        sentence1 = sentence_pair[0][0]
        sentence2 = sentence_pair[0][1]
        try:
            sentence1 = nlp.parseText(sentence1)
            sentence2 = nlp.parseText(sentence2)
        except Exception:
            logging.warning("Error when parsing index " + str(idx))
            continue
        corpus.extend([sentence1['sentences'][0]['lemmas'], sentence2['sentences'][0]['lemmas']])
        lemma_matrix.append([sentence1['sentences'][0]['lemmas'], sentence2['sentences'][0]['lemmas']])
        parse_tree_matrix.append([sentence1['sentences'][0]['parsetree'], sentence2['sentences'][0]['parsetree']])
        parse_result_matrix.append([sentence1, sentence2])
        label_matrix.append(sentence_pair[1])
        if idx % 100 == 0:
            logging.info('Parsed ' + str(idx) + " sentence pairs")
    pdump([corpus, lemma_matrix, parse_tree_matrix, parse_result_matrix, label_matrix],
          training_path_base + "all_input.pickle")


save_input_matrices(training_matrix)

logging.info("Start loading input file")
[corpus, lemma_matrix, parse_tree_matrix, parse_result_matrix, label_matrix] = pload(
    training_path_base + "all_input.pickle")
logging.info("Loaded!")

# Calculate idf first
# idf = idf.inverse_document_frequencies(corpus)
# pdump(idf, training_path_base + "idf.pickle")

# Pair features #
# N-gram features and Wordnet Agumented word overlap
# ngram_features = []
# wordnet_overlap_feature = []
# for sentence_pair in lemma_matrix:
#     sentence1 = sentence_pair[0]
#     sentence2 = sentence_pair[1]
#     gram1 = ngram.ngram_score(sentence1, sentence2, 1)
#     gram2 = ngram.ngram_score(sentence1, sentence2, 2)
#     gram3 = ngram.ngram_score(sentence1, sentence2, 3)
#     gram = [gram1, gram2, gram3]
#     ngram_features.append(gram)
#     wn_score = wordnet.wn_overlap_score_harmonic(sentence1, sentence2)
#     wordnet_overlap_feature.append(wn_score)
# pdump(ngram_features, training_path_base + "ngram_feature.pickle")
# pdump(wordnet_overlap_feature, training_path_base + "wn_overlap_feature.pickle")

# Syntactic features
from traditional.pair_feature.syntactic_tree.node import Node
from traditional.pair_feature.syntactic_tree import syntactic_tree_similarity

syntactic_features = []
for sentence_pair in parse_tree_matrix:
    sentence1 = sentence_pair[0]
    sentence2 = sentence_pair[1]
    node1 = Node.fromstring(sentence1)
    node2 = Node.fromstring(sentence2)
    score = syntactic_tree_similarity.normalized_simialrity_score(node1, node2)
    syntactic_features.append(score)
pdump(syntactic_features, training_path_base + "syntactic_features.pickle")

# Alignment features
from traditional.pair_feature.word_alignment import aligner
from traditional.pair_feature.word_alignment.similarity import *

alignment_features = []
for sentence_pair in parse_result_matrix:
    sentence1 = sentence_pair[0]
    sentence2 = sentence_pair[1]
    alignment_result = aligner.align(sentence1, sentence2)
    alignment_score = alignment_similarity(alignment_result)
    noun_alignment_score = pos_alignment_similarity(alignment_result, wn.NOUN)
    verb_alignment_score = pos_alignment_similarity(alignment_result, wn.VERB)
    adj_alignment_score = pos_alignment_similarity(alignment_result, wn.ADJ)
    adv_alignment_score = pos_alignment_similarity(alignment_result, wn.ADV)
    alignment_features.append(
        [alignment_score, noun_alignment_score, verb_alignment_score, adj_alignment_score, adv_alignment_score])
pdump(alignment_features, training_path_base + "alignment_feature.pickle")
