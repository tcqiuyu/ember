from gensim.models.keyedvectors import KeyedVectors
import datetime
import logging


class WordEmbeddingModelLoader():
    def __init__(self, base_path):
        logging.basicConfig(level=logging.DEBUG,
                            format="%(levelname)s: %(asctime)s %(filename)s[line:%(lineno)d] %(message)s")
        # self.word2vec = self.load(base_path + "/model/deeplearning/GoogleNews-vectors-negative300.bin.gz", True)
        # self.glove = self.load(base_path + "/model/deeplearning/glove_300d.word2vec")
        # self.paragram_sl999 = self.load(base_path + "/model/deeplearning/paragram_sl999.word2vec")
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


def word2vec_feature(tokens):
    pass


def glove_feature(tokens):
    pass


def paragram_feature(tokens):
    pass


if __name__ == '__main__':
    import os

    # print(os.getcwd())
    # print()
    model_loader = WordEmbeddingModelLoader("/home/yqiu/Dropbox/Workspace/2017/ember")
    model = model_loader.paragram_ws353

    print(model_loader.paragram_ws353.most_similar(positive=['woman', 'king'], negative=['man']))
