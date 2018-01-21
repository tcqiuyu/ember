from nltk import ngrams


def ngram_score(tokenlist_1, tokenlist_2, n):
    """
    Calculate ngram overlap score

    :param tokenlist_1:
    :param tokenlist_2:
    :param n:
    :return:
    """

    grams_1 = ngrams(tokenlist_1, n)
    grams_2 = ngrams(tokenlist_2, n)
    s1 = []
    s2 = []
    for gram in grams_1:
        s1.append(gram)
    for gram in grams_2:
        s2.append(gram)

    overlap = set(s1).intersection(s2)
    if overlap == 0:
        return 0
    score = 2 / (len(s1) / len(overlap) + len(s2) / len(overlap))
    return score
