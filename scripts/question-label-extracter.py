import os

data_root = "../rawData/"

nlsy_dict_path = data_root + "NLSY97/NLSY97_Public/NLSY97_Public_Data_Dictionary.xls"
addHealth_dicts_path = data_root + "Add Health/"

from xlrd import open_workbook
from rake_nltk import Rake

from nltk.corpus import stopwords

stop_words = stopwords.words('english')


def extract_nlsy_dict():
    nlsy_dict = {}
    wb = open_workbook(nlsy_dict_path)
    for sh in wb.sheets():
        for rowx in range(sh.nrows):
            refNumber = sh.cell_value(rowx, 1)
            label = sh.cell_value(rowx, 3)
            nlsy_dict[refNumber] = label
    return nlsy_dict


def extract_addhealth_dict():
    addHealth_dict = {}
    for subdir, dir, files in os.walk(addHealth_dicts_path):
        for file in files:
            if file.find("Dictionary") != -1 and file.endswith("xls"):
                file_path = os.path.join(subdir, file)
                wb = open_workbook(file_path)
                for sh in wb.sheets():
                    for rowx in range(sh.nrows):
                        refNumber = sh.cell_value(rowx, 1)
                        label = sh.cell_value(rowx, 3)
                        addHealth_dict[refNumber] = label
    return addHealth_dict


def extract_keyword(str):
    r = Rake()
    r.extract_keywords_from_text(str)
    print r.get_ranked_phrases_with_scores()


def semantic_compare(str1, str2):
    return

def tokenize_sentence(stop_words, sentence):
    import re
    return [word for word in re.split("[ \-_]", sentence.lower()) if word not in stop_words]

def tokenize_sentences(stop_words, sentences):
    import re
    return [[word for word in re.split("[ \-_]", sentence.lower()) if word not in stop_words]
            for sentence in sentences]


if __name__ == '__main__':
    nlsy_dict = extract_nlsy_dict()
    add_health_dict = extract_addhealth_dict()
    document = [""]

    for val in nlsy_dict.values():
        document.append(val)
    print len(nlsy_dict)
    for val in add_health_dict.values():
        document.append(val)
    print len(add_health_dict)

    texts = tokenize_sentences(stop_words, document)
    from collections import defaultdict

    frequency = defaultdict(int)
    for text in texts:
        for token in text:
            frequency[token] += 1

    texts = [[token for token in text if frequency[token] > 1 and token != ""]
             for text in texts]

    print texts[15]
    print texts[4521]
    # from pprint import pprint

    # pprint(texts)

    from gensim import corpora, models, similarities

    dictionary = corpora.Dictionary(texts)
    dictionary.save("./output/addhealth.dict")

    corpus = [dictionary.doc2bow(text) for text in texts]
    corpora.MmCorpus.serialize("./output/addhealth.mm", corpus)

    lsi = models.LsiModel(corpus=corpus, id2word=dictionary, num_topics=500)

    test = "R EVER HAVE SEX?"

    vec_bow = dictionary.doc2bow(test.lower().split())
    vec_lsi = lsi[vec_bow]
    print
    print(vec_lsi)

    index = similarities.MatrixSimilarity(lsi[corpus])
    index.save("./output/addhealth.index")

    sims = index[vec_lsi]

    sims = sorted(enumerate(sims), key=lambda item: -item[1])
    print(sims)

# print wn.synsets('dog')
#
# extract_keyword("R EVER HAVE SEX? 1997")
# extract_keyword("S24Q1 EVER HAVE SEX - W1")
#
# str = "S24Q1 EVER HAVE SEX - W1"
# stop_words = set(stopwords.words('english'))
#
# n = wn.synsets("S24Q1 EVER HAVE SEX-W1")
# g = wn.synsets("R EVER HAVE SEX? 1997")
#
# print n
# print g
# print max(i.path_similarity(n[0]) for i in g)
#
# # semantic_compare()
