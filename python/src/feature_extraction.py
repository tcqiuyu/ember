import numpy as np
import gc

from traditional.pair_feature import ngram
from traditional.pair_feature import wordnet
from traditional import idf
from preprocessing import corenlp as nlp

import logging

from utils import pload, pdump

training_path_base = "../../data/training/"

logging.basicConfig(level=logging.INFO,
                    format="%(levelname)s: %(asctime)s %(filename)s[line:%(lineno)d] %(message)s")

# Obtain training data
training_matrix = pload(training_path_base + "training_data.pickle")

sentence_pair_matrix = []
label_matrix = []

# Using Stanford NLP to parsing the sentence pair
lemma_matrix = []
parse_tree_matrix = []  # for syntactic parse features
corpus = [[], []]  # for idf, bow, word embedding
parse_result_matrix = []  # for alignment features
dep_matrix = [[], []]


def parse_dependency(dep_triple):
    return " ".join(['|'.join([token.split("-")[0].split(":")[0] for token in word_dependency]) for word_dependency in
                     dep_triple])


def save_input_matrices(training_matrix, path):
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
    tokenized_corpus_1 = [lemma_pair[0] for lemma_pair in lemma_matrix]
    tokenized_corpus_2 = [lemma_pair[1] for lemma_pair in lemma_matrix]
    tokenized_corpus = [tokenized_corpus_1, tokenized_corpus_2]
    pdump([corpus, tokenized_corpus, lemma_matrix, parse_tree_matrix, parse_result_matrix, dep_matrix, label_matrix],
          path)


save_input_matrices(training_matrix, training_path_base + "all_input.pickle")

logging.info("Start loading input file")
[corpus, tokenized_corpus, lemma_matrix, parse_tree_matrix, parse_result_matrix, dep_matrix, label_matrix] = pload(
    training_path_base + "all_input.pickle")
logging.info("Loaded!")

# Calculate idf first
logging.info("Start calculating idf matrix")
idf_1 = idf.inverse_document_frequencies(tokenized_corpus[0])
idf_2 = idf.inverse_document_frequencies(tokenized_corpus[1])
pdump([idf_1, idf_2], training_path_base + "idf.pickle")
logging.info("IDF matrix saved!")

# Pair features #
# N-gram features and Wordnet Agumented word overlap
ngram_features = []
wordnet_overlap_feature = []
logging.info("Start calculating N-gram features and Wordnet Agumented word overlap")
for idx, sentence_pair in enumerate(lemma_matrix):
    if idx % 100 == 0:
        logging.info("Parsed " + str(idx) + " sentence pairs")
    sentence1 = sentence_pair[0]
    sentence2 = sentence_pair[1]
    gram1 = ngram.ngram_score(sentence1, sentence2, 1)
    gram2 = ngram.ngram_score(sentence1, sentence2, 2)
    gram3 = ngram.ngram_score(sentence1, sentence2, 3)
    gram = [gram1, gram2, gram3]
    ngram_features.append(gram)
    wn_score = wordnet.wn_overlap_score_harmonic(sentence1, sentence2)
    wordnet_overlap_feature.append(wn_score)
pdump(ngram_features, training_path_base + "ngram_feature.pickle")
logging.info("N-gram feature matrix saved!")
pdump(wordnet_overlap_feature, training_path_base + "wn_overlap_feature.pickle")
logging.info("Wordnet overlap feature matrix saved!")

# Syntactic features
from traditional.pair_feature.syntactic_tree.node import Node
from traditional.pair_feature.syntactic_tree import syntactic_tree_similarity

syntactic_features = []
for idx, sentence_pair in enumerate(parse_tree_matrix):
    # if idx <= 247:
    #     continue
    sentence1 = sentence_pair[0]
    sentence2 = sentence_pair[1]
    node1 = Node.fromstring(sentence1)
    node2 = Node.fromstring(sentence2)
    score = syntactic_tree_similarity.normalized_simialrity_score(node1, node2)
    if idx % 100 == 0:
        logging.info("Parsed " + str(idx) + " syntatic feature ")
    syntactic_features.append(score)
pdump(syntactic_features, training_path_base + "syntactic_features.pickle")

# Alignment features
from traditional.pair_feature.word_alignment import aligner
from traditional.pair_feature.word_alignment.similarity import *

alignment_features = []
logging.info("Start calculating Alignment features")
for idx, sentence_pair in enumerate(parse_result_matrix):
    if idx % 100 == 0:
        logging.info("Parsed " + str(idx) + " alignment features")
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
logging.info("Alignment feature matrix saved!")

# Single features #
# BoW features
from python.src.traditional.single_feature.single_feature_factory import *

#
idf = pload(training_path_base + "idf.pickle")
idf_1 = idf[0]
idf_2 = idf[1]
corp = corpus[0] + corpus[1]
bow = bow_feature(corp)
bow_matrix = bow[0]
bow_vocab = bow[1]
bow_1 = bow_matrix[:len(corpus[0])]
bow_2 = bow_matrix[len(corpus[0]):]
idf_vector_1 = [0] * bow_1.shape[1]
idf_vector_2 = [0] * bow_2.shape[1]
for vocab in bow_vocab:
    index = bow_vocab[vocab]
    try:
        vocab_idf_1 = idf_1[vocab]
        idf_vector_1[index] = vocab_idf_1
        vocab_idf_2 = idf_2[vocab]
        idf_vector_2[index] = vocab_idf_2
    except KeyError:
        pass
bow_1 = np.multiply(bow_1, idf_vector_1)
bow_2 = np.multiply(bow_2, idf_vector_2)
print(bow_1.shape)
print(bow_2.shape)

# # joblib.dump([bow_1, bow_2], training_path_base+"bow.features")
pdump([bow_1, bow_2], training_path_base + "bow.pickle")

# Dependency Triple Features
dep_1 = dep_matrix[0]
dep_2 = dep_matrix[1]
deps_corpus = dep_1 + dep_2
dep_triple_features = bow_feature(deps_corpus)[0]
dep_triple_1 = dep_triple_features[:len(dep_1)]
dep_triple_2 = dep_triple_features[len(dep_1):]

pdump([dep_triple_1, dep_triple_2], training_path_base + "dep_triple.pickle")

# Word Embedding Features
from traditional.single_feature.word_embedding_features import *

model_loader = WordEmbeddingModelLoader("/home/yqiu/Dropbox/Workspace/2017/ember")

# word2vec
vector_word2vec = []
sentence_vector_1 = []
sentence_vector_2 = []
for lemma_pair in lemma_matrix:
    lemma_1 = lemma_pair[0]
    lemma_2 = lemma_pair[1]
    sentence_vector_1.append(word_embedding_feature(lemma_1, model_loader.word2vec, idf_1))
    sentence_vector_2.append(word_embedding_feature(lemma_2, model_loader.word2vec, idf_2))
vector_word2vec.append([sentence_vector_1, sentence_vector_2])
pdump(vector_word2vec, training_path_base + "word_embedding_word2vec.pickle")

# glove
vector_glove = []
sentence_vector_1 = []
sentence_vector_2 = []
for lemma_pair in lemma_matrix:
    lemma_1 = lemma_pair[0]
    lemma_2 = lemma_pair[1]
    sentence_vector_1.append(word_embedding_feature(lemma_1, model_loader.glove, idf_1))
    sentence_vector_2.append(word_embedding_feature(lemma_2, model_loader.glove, idf_2))
vector_glove.append([sentence_vector_1, sentence_vector_2])
pdump(vector_glove, training_path_base + "word_embedding_glove.pickle")

# paragram_sl999
vector_paragram999 = []
sentence_vector_1 = []
sentence_vector_2 = []
for lemma_pair in lemma_matrix:
    lemma_1 = lemma_pair[0]
    lemma_2 = lemma_pair[1]
    sentence_vector_1.append(word_embedding_feature(lemma_1, model_loader.paragram_sl999, idf_1))
    sentence_vector_2.append(word_embedding_feature(lemma_2, model_loader.paragram_sl999, idf_2))
vector_paragram999.append([sentence_vector_1, sentence_vector_2])
pdump(vector_paragram999, training_path_base + "word_embedding_paragram999.pickle")

# paragram_ws353
vector_paragram353 = []
sentence_vector_1 = []
sentence_vector_2 = []
for lemma_pair in lemma_matrix:
    lemma_1 = lemma_pair[0]
    lemma_2 = lemma_pair[1]
    sentence_vector_1.append(word_embedding_feature(lemma_1, model_loader.paragram_ws353, idf_1))
    sentence_vector_2.append(word_embedding_feature(lemma_2, model_loader.paragram_ws353, idf_2))
vector_paragram353.append([sentence_vector_1, sentence_vector_2])
pdump(vector_paragram353, training_path_base + "word_embedding_paragram353.pickle")

# Single sentence features dimension deduction
single_feature_matrix = []

# Loading features

# Bag of words
bow_feature = pload(training_path_base + "bow.pickle")
bow_1_feature = np.asarray(bow_feature[0])
bow_2_feature = np.asarray(bow_feature[1])

# Dependency triple
dep_feature = pload(training_path_base + "dep_triple.pickle")
dep_1_feature = np.asarray(dep_feature[0])
dep_2_feature = np.asarray(dep_feature[1])

# Word embedding features
word2vec_feature = pload(training_path_base + "word_embedding_word2vec.pickle")
word2vec_1_feature = word2vec_feature[0][0]
word2vec_2_feature = word2vec_feature[0][1]
glove_feature = pload(training_path_base + "word_embedding_glove.pickle")
glove_1_feature = glove_feature[0][0]
glove_2_feature = glove_feature[0][1]
paragram353_feature = pload(training_path_base + "word_embedding_paragram353.pickle")
paragram353_1_feature = paragram353_feature[0][0]
paragram353_2_feature = paragram353_feature[0][1]
paragram999_feature = pload(training_path_base + "word_embedding_paragram999.pickle")
paragram999_1_feature = paragram999_feature[0][0]
paragram999_2_feature = paragram999_feature[0][1]

s1 = []
for f1, f2, f3, f4, f5, f6 in zip(bow_1_feature, dep_1_feature, word2vec_1_feature, glove_1_feature,
                                  paragram353_1_feature, paragram999_1_feature):
    s1.append(np.concatenate((f1, f2, f3, f4, f5, f6)))

s2 = []
for f1, f2, f3, f4, f5, f6 in zip(bow_2_feature, dep_2_feature, word2vec_2_feature, glove_2_feature,
                                  paragram353_2_feature, paragram999_2_feature):
    s2.append(np.concatenate((f1, f2, f3, f4, f5, f6)))

y = np.asarray(label_matrix)

s1 = np.asarray(s1)
gc.collect()
s2 = np.asarray(s2)
gc.collect()

s1_splited = np.array_split(s1, 100, axis=0)
s2_splited = np.array_split(s2, 100, axis=0)

del s1, s2
del bow_1_feature, dep_1_feature, word2vec_1_feature, glove_1_feature, paragram353_1_feature, paragram999_1_feature
del bow_2_feature, dep_2_feature, word2vec_2_feature, glove_2_feature, paragram353_2_feature, paragram999_2_feature
gc.collect()

from traditional.single_feature.kernels import *

linear = []
stat = []
non_linear = []

for X1, X2 in zip(s1_splited, s2_splited):
    linear.append(linear_kernel(X1, X2))
    stat.append(stat_kernel(X1, X2))
    non_linear.append(non_linear_kernel(X1, X2))
linear = np.concatenate(linear)
non_linear = np.concatenate(non_linear)
stat = np.concatenate(stat)
single_feature = np.hstack((linear, stat, non_linear))

pdump(single_feature, training_path_base + "single_feature.pickle")

# Integrate all traditional features
# Pair sentence features
# Ngram features
feat_ngram = np.asarray(pload(training_path_base + "ngram_feature.pickle"))

# Wordnet overlap feature
feat_wn_overlap = np.asarray(pload(training_path_base + "wn_overlap_feature.pickle")).reshape(-1, 1)

# Syntactic tree feature
feat_synt_tree = np.asarray(pload(training_path_base + "syntactic_features.pickle")).reshape(-1, 1)

# Alignment feature
feat_alignment = np.asarray(pload(training_path_base + "alignment_feature.pickle"))

# Single sentence features
feat_single = pload(training_path_base + "single_feature.pickle")

feat_all = np.hstack((feat_ngram, feat_wn_overlap, feat_synt_tree, feat_alignment, feat_single))

label = [float(lab) for lab in label_matrix]
label = np.asarray(label)
pdump([feat_all, label], training_path_base + "traditional_features.pickle")
