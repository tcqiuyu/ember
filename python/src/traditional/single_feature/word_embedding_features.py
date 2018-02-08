from gensim.models.keyedvectors import KeyedVectors
import datetime
import logging
import numpy as np


class WordEmbeddingModelLoader:
    def __init__(self, base_path):
        logging.basicConfig(level=logging.DEBUG,
                            format="%(levelname)s: %(asctime)s %(filename)s[line:%(lineno)d] %(message)s")
        self.word2vec = self.load(base_path + "/model/deeplearning/GoogleNews-vectors-negative300.bin.gz", True)
        self.glove = self.load(base_path + "/model/deeplearning/glove_300d.word2vec")
        self.paragram_sl999 = self.load(base_path + "/model/deeplearning/paragram_sl999.word2vec")
        self.paragram_ws353 = self.load(base_path + "/model/deeplearning/paragram_ws353.word2vec")

    def load(self, path, binary=False):
        name = path.split("/")[-1]
        logging.info("Start loading " + name)
        start = datetime.datetime.now().replace(microsecond=0)
        model = KeyedVectors.load_word2vec_format(path, binary=binary)
        end = datetime.datetime.now().replace(microsecond=0)
        time = end - start
        logging.info("Loading " + name + "complete, elapsed time: " + str(time))

        # print("Loading ", path.split("/")[-1], " finished, time cost:", end - start)
        return model


def word_embedding_feature(tokenized_sentence, model, idf_dict):
    sentence_vector = []

    for token in tokenized_sentence:
        try:
            word_vector = model[token] * idf_dict[token]
        except KeyError:
            word_vector = np.random.uniform(-0.1, 0.1, 300) * idf_dict[token]
        sentence_vector.append(word_vector)

    sentence_vector = np.asarray(sentence_vector)
    avg = sentence_vector.mean(axis=0)
    min = sentence_vector.min(axis=0)
    max = sentence_vector.max(axis=0)
    word_embedding_feature = np.concatenate((avg, min, max))
    return word_embedding_feature


if __name__ == '__main__':
    import os

    # print(os.getcwd())
    # print()
    model_loader = WordEmbeddingModelLoader("/home/yqiu/Dropbox/Workspace/2017/ember")
    paragram = model_loader.paragram_ws353
    a = word_embedding_feature(["hello", "world"], paragram)
    vec = paragram.word_vec("hello")
    print(model_loader.paragram_ws353.most_similar(positive=['woman', 'king'], negative=['man']))
