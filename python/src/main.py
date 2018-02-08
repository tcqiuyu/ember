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
corpus = [[], []]  # for idf, bow, word embedding
parse_result_matrix = []  # for alignment features
dep_matrix = [[], []]


def parse_dependency(dep_triple):
    return " ".join(['|'.join([token.split("-")[0].split(":")[0] for token in word_dependency]) for word_dependency in
                     dep_triple])


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
        corpus[0].append(sentence1['sentences'][0]['text'])
        corpus[1].append(sentence2['sentences'][0]['text'])

        # corpus.extend([sentence1['sentences'][0]['lemmas'], sentence2['sentences'][0]['lemmas']])
        lemma_matrix.append([sentence1['sentences'][0]['lemmas'], sentence2['sentences'][0]['lemmas']])
        parse_tree_matrix.append([sentence1['sentences'][0]['parsetree'], sentence2['sentences'][0]['parsetree']])
        parse_result_matrix.append([sentence1, sentence2])
        dep_matrix[0].append(parse_dependency(sentence1['sentences'][0]['dependencies']))
        dep_matrix[1].append(parse_dependency(sentence2['sentences'][0]['dependencies']))
        label_matrix.append(sentence_pair[1])
        if idx % 100 == 0:
            logging.info('Parsed ' + str(idx) + " sentence pairs")
    pdump([corpus, lemma_matrix, parse_tree_matrix, parse_result_matrix, label_matrix],
          training_path_base + "all_input.pickle")


# save_input_matrices(training_matrix)

logging.info("Start loading input file")
[corpus, lemma_matrix, parse_tree_matrix, parse_result_matrix, dep_matrix, label_matrix] = pload(
    training_path_base + "all_input.pickle")
logging.info("Loaded!")

# Calculate idf first
# logging.info("Start calculating idf matrix")
# idf_1 = idf.inverse_document_frequencies(corpus[0])
# idf_2 = idf.inverse_document_frequencies(corpus[1])
# pdump([idf_1, idf_2], training_path_base + "idf.pickle")
# logging.info("IDF matrix saved!")

# Pair features #
# N-gram features and Wordnet Agumented word overlap
# ngram_features = []
# wordnet_overlap_feature = []
# logging.info("Start calculating N-gram features and Wordnet Agumented word overlap")
# for idx, sentence_pair in enumerate(lemma_matrix):
#     if idx % 100 == 0:
#         logging.info("Parsed " + str(idx) + " sentence pairs")
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
# logging.info("N-gram feature matrix saved!")
# pdump(wordnet_overlap_feature, training_path_base + "wn_overlap_feature.pickle")
# logging.info("Wordnet overlap feature matrix saved!")

# Syntactic features
# from traditional.pair_feature.syntactic_tree.node import Node
# from traditional.pair_feature.syntactic_tree import syntactic_tree_similarity
#
# syntactic_features = []
# for idx, sentence_pair in enumerate(parse_tree_matrix):
#     # if idx <= 247:
#     #     continue
#     sentence1 = sentence_pair[0]
#     sentence2 = sentence_pair[1]
#     node1 = Node.fromstring(sentence1)
#     node2 = Node.fromstring(sentence2)
#     score = syntactic_tree_similarity.normalized_simialrity_score(node1, node2)
#     if idx % 100 == 0:
#         logging.info("Parsed " + str(idx) + " syntatic feature ")
#     syntactic_features.append(score)
# pdump(syntactic_features, training_path_base + "syntactic_features.pickle")

# Alignment features
# from traditional.pair_feature.word_alignment import aligner
# from traditional.pair_feature.word_alignment.similarity import *
#
# alignment_features = []
# logging.info("Start calculating Alignment features")
# for idx, sentence_pair in enumerate(parse_result_matrix):
#     if idx % 100 == 0:
#         logging.info("Parsed " + str(idx) + " alignment features")
#     sentence1 = sentence_pair[0]
#     sentence2 = sentence_pair[1]
#     alignment_result = aligner.align(sentence1, sentence2)
#     alignment_score = alignment_similarity(alignment_result)
#     noun_alignment_score = pos_alignment_similarity(alignment_result, wn.NOUN)
#     verb_alignment_score = pos_alignment_similarity(alignment_result, wn.VERB)
#     adj_alignment_score = pos_alignment_similarity(alignment_result, wn.ADJ)
#     adv_alignment_score = pos_alignment_similarity(alignment_result, wn.ADV)
#     alignment_features.append(
#         [alignment_score, noun_alignment_score, verb_alignment_score, adj_alignment_score, adv_alignment_score])
# pdump(alignment_features, training_path_base + "alignment_feature.pickle")
# logging.info("Alignment feature matrix saved!")


# Single features #
# BoW features
from python.src.traditional.single_feature.single_feature_factory import *

idf = pload(training_path_base + "idf.pickle")
idf_1 = idf[0]
idf_2 = idf[1]
corp = corpus[0] + corpus[1]
bow = bow_feature(corp)[0]
bow_1 = bow[:len(corpus[0])]
bow_2 = bow[len(corpus[0]):]

print(bow_1.shape)
print(bow_2.shape)

# Dependency Triple Features
dep_1 = dep_matrix[0]
dep_2 = dep_matrix[1]
deps_corpus = dep_1 + dep_2
dep_triple_features = bow_feature(deps_corpus)[0]
dep_triple_1 = dep_triple_features[:len(dep_1)]
dep_triple_2 = dep_triple_features[len(dep_1):]

print(dep_triple_1.shape)
print(dep_triple_2.shape)

# Word Embedding Features
