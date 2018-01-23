from nltk.corpus import wordnet as wn
from traditional.pair_feature.wordnet import wn_overlap_score

if __name__ == '__main__':
    sentence1 = "I am higher."
    sentence2 = "You are fat."
    # print(ngram_score(sentence1, sentence2, 1))
    w_high = wn.synset("high.a.1")
    # print(wn_word_sentence_score(w_high, sentence1))
    print(wn_overlap_score(sentence1, sentence2))
