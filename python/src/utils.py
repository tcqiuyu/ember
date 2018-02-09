import pickle
import logging


def pload(path):
    logging.info("Loading pickle: " + path)
    f = open(path, "rb")
    out = pickle.load(f)
    f.close()
    logging.info("Finish loading pickle: " + path)
    return out


def pdump(obj, path):
    f = open(path, "wb")
    pickle.dump(obj, f)
    f.close()