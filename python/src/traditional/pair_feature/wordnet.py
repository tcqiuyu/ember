import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer


def get_wordnet_pos(treebank_tag):
    """
    Convert treebank tag to wordnet pos tag

    :param treebank_tag:
    :return: wordnet pos tag
    """
    if treebank_tag.startswith('J'):
        return wn.ADJ
    elif treebank_tag.startswith('V'):
        return wn.VERB
    elif treebank_tag.startswith('N'):
        return wn.NOUN
    elif treebank_tag.startswith('R'):
        return wn.ADV
    else:
        return ''


def _wn_word_sentence_score(wn_tagged_word, tokened_sentence):
    """
    Cacluate wordnet-based similarity score between a word and a given sentence
    Used in @wn_overlap_score

    :param wn_tagged_word:
    :param tokened_sentence:
    :return:
    """

    word1 = wn_tagged_word.name().split(".")[0]  # get the plain word text from the input
    score = 0
    lemmatizer = WordNetLemmatizer()

    if word1 in tokened_sentence:  # If the word exists in the given sentence, then the score would be 1
        return 1
    else:  # otherwise, calculate the maximum similarity score among the given word and all words in the sentence
        tagged_list = nltk.pos_tag(tokened_sentence)

        for word2 in tagged_list:
            pos = get_wordnet_pos(word2[1])
            if pos is "":
                continue
            lemma = lemmatizer.lemmatize(word2[0], pos)

            tagged_word2 = lemma + "." + pos + ".1"

            sim = wn_tagged_word.path_similarity(wn.synset(tagged_word2))
            if sim is not None:
                score = max(score, sim)
    return score


def wn_overlap_score(sentence1, sentence2):
    """
    Calculate wordnet-augmented word overlap similarity score between sentences.
    Note: @wn_overlap_score(s1, s2) might not equal to @wn_overlap_score(s2, s1).
    We calculate harmonic mean of them to get the final similarity score

    :param sentence1:
    :param sentence2:
    :return:
    """
    score = 0

    # Tokenize two sentences
    tokened_sentence1 = word_tokenize(sentence1)
    tokened_sentence2 = word_tokenize(sentence2)

    # Pos-tagged two tokenized sentences
    tagged_wordlist1 = nltk.pos_tag(tokened_sentence1)
    tagged_wordlist2 = nltk.pos_tag(tokened_sentence2)

    # Filtered list
    filtered_tagged_wordlist1 = []
    filtered_wordlist2 = []

    lemmatizer = WordNetLemmatizer()

    for token1 in tagged_wordlist1:
        pos1 = get_wordnet_pos(token1[1])  # get wordnet pos tag
        if pos1 is "":
            continue
        lemma1 = lemmatizer.lemmatize(token1[0], pos1)  # get lemma from the word and its pos tag
        wn_tagged_word = lemma1 + "." + pos1 + ".1"  # TODO: Here we just assume the most popular meaning
        filtered_tagged_wordlist1.append(wn_tagged_word)

    # For sentence2, we just filtered and lemmatize non-content word
    # because it will be pos tagged in @wn_word_sentence_score
    for token2 in tagged_wordlist2:
        pos2 = get_wordnet_pos(token2[1])
        if pos2 is "":
            continue
        lemma2 = lemmatizer.lemmatize(token2[0], pos2)
        filtered_wordlist2.append(lemma2)

    for wn_tagged_word in filtered_tagged_wordlist1:
        score += _wn_word_sentence_score(wn.synset(wn_tagged_word), filtered_wordlist2)

    score = score / len(filtered_wordlist2)
    return score
