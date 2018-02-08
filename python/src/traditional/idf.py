import math


def inverse_document_frequencies(tokenized_documents):
    idf_values = {}
    all_tokens_set = set([item for sublist in tokenized_documents for item in sublist])
    for tkn in all_tokens_set:
        contains_token = map(lambda doc: tkn in doc, tokenized_documents)
        idf_values[tkn] = 1 + math.log(len(tokenized_documents) / (sum(contains_token)))
    return idf_values


if __name__ == '__main__':
    inverse_document_frequencies([["Hello", "world"], ["Hello", "morning"]])
