import numpy as np
import os
import csv
import logging
from traditional.single_feature.word_embedding_features import *
from python.src.traditional.single_feature.single_feature_factory import *

from traditional.regression import EnsembleRegressor
from preprocessing import corenlp as nlp

from utils import *

logging.basicConfig(level=logging.INFO,
                    format="%(levelname)s: %(asctime)s %(filename)s[line:%(lineno)d] %(message)s")
training_path_base = "../../data/training/"
predicting_path_base = "../../data/predicting/"


# Loading features
# [traditional_features, label] = pload(training_path_base + "traditional_features.pickle")


# ensem_regressor = EnsembleRegressor()
# ensem_regressor.random_forest(traditional_features, label)
# ensem_regressor.gradient_boosting(traditional_features, label)
# ensem_regressor.xgboost(traditional_features, label)
# ensem_regressor.save_model(training_path_base+"regr_model.pickle")
# ensem_regressor.load_model(training_path_base+"regr_model.pickle")

def extract_main_text(path):
    matrix = []
    with open(path, mode='r') as csvfile:
        # logging.info("Parsing " + csvfile)
        rows = csv.reader(csvfile, delimiter='|', quoting=csv.QUOTE_NONE)
        for row in rows:
            item = next(item for item in row[1:] if item != "")
            matrix.append(item)
            # if row != "":
            #     matrix.append(row[1])
            # else:
            #     matrix.append(row[2])
    return matrix


def parse_dependency(dep_triple):
    return " ".join(['|'.join([token.split("-")[0].split(":")[0] for token in word_dependency]) for word_dependency in
                     dep_triple])


def save_input_matrices(training_matrix, path):
    corpus = []
    lemma_matrix = []
    parse_tree_matrix = []
    parse_result_matrix = []
    dep_matrix = []

    for idx, sentence in enumerate(training_matrix):
        try:
            sentence1 = nlp.parseText(sentence)
        except Exception:
            logging.warning("Error when parsing index " + str(idx))
            continue
        corpus.append(sentence1['sentences'][0]['text'])

        lemma_matrix.append(sentence1['sentences'][0]['lemmas'])
        parse_tree_matrix.append(sentence1['sentences'][0]['parsetree'])
        parse_result_matrix.append(sentence1)
        dep_matrix.append(parse_dependency(sentence1['sentences'][0]['dependencies']))

        if idx % 100 == 0:
            logging.info('Parsed ' + str(idx) + " sentence pairs")
    tokenized_corpus = [lemma for lemma in lemma_matrix]
    pdump([corpus, tokenized_corpus, lemma_matrix, parse_tree_matrix, parse_result_matrix, dep_matrix],
          path)
    return [corpus, tokenized_corpus, lemma_matrix, parse_tree_matrix, parse_result_matrix, dep_matrix]


add_path = "../../data/intermediate/add_health_interm"
nlsy_path = "../../data/intermediate/nlsy_interm"


# add_health = extract_main_text(add_path)
# nlsy = extract_main_text(nlsy_path)
# logging.info("Finished")

# add_health = save_input_matrices(add_health, predicting_path_base + "add_health.pickle")
# nlsy = save_input_matrices(nlsy, predicting_path_base + "nlsy.pickle")

# Constructing features
def construct_features(name):
    logging.info("Start loading input file")
    [corpus, tokenized_corpus, lemma_matrix, parse_tree_matrix, parse_result_matrix, dep_matrix] = pload(
        predicting_path_base + name + ".pickle")
    logging.info("Loaded!")

    from traditional.idf import inverse_document_frequencies

    # IDF matrix
    logging.info("Start calculating idf matrix")
    idf = inverse_document_frequencies(tokenized_corpus)
    pdump(idf, predicting_path_base + "idf_" + name + ".pickle")

    # Single sentence feature
    # BoW features

    # idf = pload(predicting_path_base + "idf" + name + ".pickle")
    bow = bow_feature(corpus)
    bow_matrix = bow[0]
    bow_vocab = bow[1]
    idf_vector = [0] * bow_matrix.shape[1]
    for vocab in bow_vocab:
        index = bow_vocab[vocab]
        try:
            vocab_idf = idf[vocab]
            idf_vector[index] = vocab_idf
        except KeyError:
            pass
    bow_matrix = np.multiply(bow_matrix, idf_vector)
    pdump(bow_matrix, predicting_path_base + "bow_" + name + ".pickle")

    # Dependency Triple Features
    dep = dep_matrix
    dep_triple_features = bow_feature(dep)[0]
    pdump(dep_triple_features, predicting_path_base + "dep_" + name + ".pickle")

    # Word Embedding Features

    model_loader = WordEmbeddingModelLoader("/home/yqiu/Dropbox/Workspace/2017/ember")
    idf = pload(predicting_path_base + "idf_" + name + ".pickle")

    # word2vec
    sentence_vector = []
    for lemma in lemma_matrix:
        sentence_vector.append(word_embedding_feature(lemma, model_loader.word2vec, idf))
    pdump(sentence_vector, predicting_path_base + "word2vec_" + name + ".pickle")

    # glove
    sentence_vector = []
    for lemma in lemma_matrix:
        sentence_vector.append(word_embedding_feature(lemma, model_loader.glove, idf))
    pdump(sentence_vector, predicting_path_base + "glove_" + name + ".pickle")

    # paragram_sl999
    sentence_vector = []
    for lemma in lemma_matrix:
        sentence_vector.append(word_embedding_feature(lemma, model_loader.paragram_sl999, idf))
    pdump(sentence_vector, predicting_path_base + "paragram_sl999_" + name + ".pickle")

    # paragram_ws353
    sentence_vector = []
    for lemma in lemma_matrix:
        sentence_vector.append(word_embedding_feature(lemma, model_loader.paragram_ws353, idf))
    pdump(sentence_vector, predicting_path_base + "paragram_ws353_" + name + ".pickle")


def concat_features(name):
    bow = pload(predicting_path_base + "bow_" + name + ".pickle")
    dep = pload(predicting_path_base + "dep_" + name + ".pickle")
    word2vec = pload(predicting_path_base + "word2vec_" + name + ".pickle")
    glove = pload(predicting_path_base + "glove_" + name + ".pickle")
    paragram_sl999 = pload(predicting_path_base + "paragram_sl999_" + name + ".pickle")
    paragram_ws353 = pload(predicting_path_base + "paragram_ws353_" + name + ".pickle")
    single_features = np.hstack((bow, dep, word2vec, glove, paragram_ws353, paragram_sl999))
    return single_features


add_health_single_feature = concat_features("add_health")
nlsy_single_feature = concat_features("nlsy")
print(add_health_single_feature.shape)
print(nlsy_single_feature.shape)

from traditional.pair_feature.ngram import *


# Pair features #
def get_ngram_feature(lemma_tokens_1, lemma_tokens_2):
    # N-gram features and Wordnet Agumented word overlap
    ngram_features = []
    wordnet_overlap_feature = []
    logging.info("Start calculating N-gram features and Wordnet Agumented word overlap")
    gram1 = ngram_score(lemma_tokens_1, lemma_tokens_2, 1)
    gram2 = ngram_score(lemma_tokens_1, lemma_tokens_2, 2)
    gram3 = ngram_score(lemma_tokens_1, lemma_tokens_2, 3)
    gram = [gram1, gram2, gram3]
    return gram


from traditional.pair_feature.wordnet import *


def get_wn_feature(lemma_tokens_1, lemma_tokens_2):
    wn_score = wn_overlap_score_harmonic(lemma_tokens_1, lemma_tokens_2)
    return wn_score


from traditional.pair_feature.syntactic_tree.node import Node
from traditional.pair_feature.syntactic_tree import syntactic_tree_similarity


def get_synt_feature(parse_tree_1, parse_tree_2):
    node1 = Node.fromstring(parse_tree_1)
    node2 = Node.fromstring(parse_tree_2)
    score = syntactic_tree_similarity.normalized_simialrity_score(node1, node2)
    return score


[corpus_add_health, tokenized_corpus_add_health, lemma_matrix_add_health, parse_tree_matrix_add_health,
 parse_result_matrix_add_health, dep_matrix_add_health] = pload(predicting_path_base + "add_health.pickle")
[corpus_nlsy, tokenized_corpus_nlsy, lemma_matrix_nlsy, parse_tree_matrix_nlsy,
 parse_result_matrix_nlsy, dep_matrix_nlsy] = pload(predicting_path_base + "nlsy.pickle")

for i in range(len(corpus_nlsy)):

print("Hello")
