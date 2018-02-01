from sklearn.feature_extraction.text import CountVectorizer
from python.src.preprocessing.corenlp import *


def bow_feature(corpus):
    vectorizer = CountVectorizer()
    matrix = vectorizer.fit_transform(corpus).todense()
    return matrix, vectorizer.vocabulary_


def dependency_feature(corpus):
    parsed_corpus = []
    vectorizer = CountVectorizer(tokenizer=(lambda x: x.split(" ")))
    for sentence in corpus:
        dependency_tree = parseText(sentence)['sentences'][0]['dependencies']
        dependency = ['|'.join([token.split("-")[0].split(":")[0] for token in word_dependency]) for word_dependency in dependency_tree]
        parsed_corpus.extend(dependency)
    matrix = vectorizer.fit_transform(parsed_corpus).todense()
    return matrix, vectorizer.vocabulary_





if __name__ == '__main__':
    sentences = ["Four men died in an accident.", "4 people are dead from a collision."]
    bow_feature(sentences)
    dependency_feature(sentences)
    pass

