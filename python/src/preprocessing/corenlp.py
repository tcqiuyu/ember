from pycorenlp import StanfordCoreNLP
import re


class StanfordNLP:
    def __init__(self):
        self.server = StanfordCoreNLP("http://localhost:9000")

    def parse(self, text):
        return self.server.annotate(text, properties={
            'annotators': 'tokenize,ssplit,pos,depparse,parse,lemma,ner',
            'outputFormat': 'json'
        })


def parseText(raw_sentence):
    parse_result = nlp_server.parse(raw_sentence)
    out = {}
    sentences = []
    sentence = {}

    dependencies = []
    for dependency in parse_result['sentences'][0]['enhancedPlusPlusDependencies']:
        dependency_dic = [dependency['dep'], dependency['governorGloss'] + "-" + str(dependency['governor']),
                          dependency['dependentGloss'] + "-" + str(dependency['dependent'])]
        dependencies.append(dependency_dic)

    parse_tree = re.subn("\n\s*", ", ", parse_result['sentences'][0]['parse'])[0]

    words = []
    for token in parse_result['sentences'][0]['tokens']:
        word = [token['word']]
        attribute = {'NamedEntityTag': token['pos'],
                     'CharacterOffsetBegin': str(token['characterOffsetBegin']),
                     'CharacterOffsetEnd': str(token['characterOffsetEnd']),
                     'PartOfSpeech': token['pos'],
                     'Lemma': token['lemma']}
        if 'normalizedNER' in token:
            attribute['NormalizedNamedEntityTag'] = token['normalizedNER']

        word.append(attribute)
        words.append(word)

    sentence['dependencies'] = dependencies
    sentence['parsetree'] = parse_tree
    sentence['text'] = raw_sentence
    sentence['words'] = words

    sentences.append(sentence)
    out['sentences'] = sentences

    return out


def nerWordAnnotator(parseResult):
    res = []
    wordIndex = 1
    for i in range(len(parseResult['sentences'][0]['words'])):
        tag = [[parseResult['sentences'][0]['words'][i][1]['CharacterOffsetBegin'],
                parseResult['sentences'][0]['words'][i][1]['CharacterOffsetEnd']], wordIndex,
               parseResult['sentences'][0]['words'][i][0], parseResult['sentences'][0]['words'][i][1]['NamedEntityTag']]
        wordIndex += 1
        if tag[3] != 'O':
            res.append(tag)
    return res


def lemmatize(parse_result):
    res = []

    word_index = 1
    for i in range(len(parse_result['sentences'][0]['words'])):
        tag = [[parse_result['sentences'][0]['words'][i][1]['CharacterOffsetBegin'],
                parse_result['sentences'][0]['words'][i][1]['CharacterOffsetEnd']], word_index,
               parse_result['sentences'][0]['words'][i][0], parse_result['sentences'][0]['words'][i][1]['Lemma']]
        word_index += 1
        res.append(tag)

    return res


def posTag(parse_result):
    res = []

    word_index = 1
    for i in range(len(parse_result['sentences'][0]['words'])):
        tag = [[parse_result['sentences'][0]['words'][i][1]['CharacterOffsetBegin'],
                parse_result['sentences'][0]['words'][i][1]['CharacterOffsetEnd']], word_index,
               parse_result['sentences'][0]['words'][i][0], parse_result['sentences'][0]['words'][i][1]['PartOfSpeech']]
        word_index += 1
        res.append(tag)

    return res


def ner(parseResult):
    nerWordAnnotations = nerWordAnnotator(parseResult)

    namedEntities = []
    currentNE = []
    currentCharacterOffsets = []
    currentWordOffsets = []

    for i in range(len(nerWordAnnotations)):

        if i == 0:
            currentNE.append(nerWordAnnotations[i][2])
            currentCharacterOffsets.append(nerWordAnnotations[i][0])
            currentWordOffsets.append(nerWordAnnotations[i][1])
            if len(nerWordAnnotations) == 1:
                namedEntities.append(
                    [currentCharacterOffsets, currentWordOffsets, currentNE, nerWordAnnotations[i - 1][3]])
                break
            continue

        if nerWordAnnotations[i][3] == nerWordAnnotations[i - 1][3] and nerWordAnnotations[i][1] == \
                nerWordAnnotations[i - 1][1] + 1:
            currentNE.append(nerWordAnnotations[i][2])
            currentCharacterOffsets.append(nerWordAnnotations[i][0])
            currentWordOffsets.append(nerWordAnnotations[i][1])
            if i == len(nerWordAnnotations) - 1:
                namedEntities.append([currentCharacterOffsets, currentWordOffsets, currentNE, nerWordAnnotations[i][3]])
        else:
            namedEntities.append([currentCharacterOffsets, currentWordOffsets, currentNE, nerWordAnnotations[i - 1][3]])
            currentNE = [nerWordAnnotations[i][2]]
            currentCharacterOffsets = []
            currentCharacterOffsets.append(nerWordAnnotations[i][0])
            currentWordOffsets = []
            currentWordOffsets.append(nerWordAnnotations[i][1])
            if i == len(nerWordAnnotations) - 1:
                namedEntities.append([currentCharacterOffsets, currentWordOffsets, currentNE, nerWordAnnotations[i][3]])

    return namedEntities


def dependencyParseAndPutOffsets(parseResult):
    """
    returns dependency parse of the sentence whhere each item is of the form
    (rel, left{charStartOffset, charEndOffset, wordNumber}, right{charStartOffset, charEndOffset, wordNumber})
    :param parseResult:
    :return:
    """
    dParse = parseResult['sentences'][0]['dependencies']
    words = parseResult['sentences'][0]['words']

    result = []

    for item in dParse:
        newItem = []

        # copy 'rel'
        newItem.append(item[0])

        # construct and append entry for 'left'
        left = item[1][0:item[1].rindex("-")]
        wordNumber = item[1][item[1].rindex("-") + 1:]
        if wordNumber.isdigit() == False:
            continue
        left += '{' + words[int(wordNumber) - 1][1]['CharacterOffsetBegin'] + ' ' + words[int(wordNumber) - 1][1][
            'CharacterOffsetEnd'] + ' ' + wordNumber + '}'
        newItem.append(left)

        # construct and append entry for 'right'
        right = item[2][0:item[2].rindex("-")]
        wordNumber = item[2][item[2].rindex("-") + 1:]
        if wordNumber.isdigit() == False:
            continue
        right += '{' + words[int(wordNumber) - 1][1]['CharacterOffsetBegin'] + ' ' + words[int(wordNumber) - 1][1][
            'CharacterOffsetEnd'] + ' ' + wordNumber + '}'
        newItem.append(right)

        result.append(newItem)

    return result


def findParents(dependencyParse, wordIndex, word):
    """
    word index assumed to be starting at 1
    the third parameter is needed because of the collapsed representation of the dependencies...

    :param dependencyParse:
    :param wordIndex:
    :param word:
    :return:
    """

    wordsWithIndices = ((int(item[2].split('{')[1].split('}')[0].split(' ')[2]), item[2].split('{')[0]) for item in
                        dependencyParse)
    wordsWithIndices = list(set(wordsWithIndices))
    wordsWithIndices = sorted(wordsWithIndices, key=lambda item: item[0])
    # print wordsWithIndices

    wordIndexPresentInTheList = False
    for item in wordsWithIndices:
        if item[0] == wordIndex:
            wordIndexPresentInTheList = True
            break

    parentsWithRelation = []

    if wordIndexPresentInTheList:
        for item in dependencyParse:
            currentIndex = int(item[2].split('{')[1].split('}')[0].split(' ')[2])
            if currentIndex == wordIndex:
                parentsWithRelation.append(
                    [int(item[1].split('{')[1].split('}')[0].split(' ')[2]), item[1].split('{')[0], item[0]])
    else:
        # find the closest following word index which is in the list
        nextIndex = 0
        for i in range(len(wordsWithIndices)):
            if wordsWithIndices[i][0] > wordIndex:
                nextIndex = wordsWithIndices[i][0]
                break
        if nextIndex == 0:
            return []  # ?
        for i in range(len(dependencyParse)):
            if int(dependencyParse[i][2].split('{')[1].split('}')[0].split(' ')[2]) == nextIndex:
                pos = i
                break
        for i in range(pos, len(dependencyParse)):
            if '_' in dependencyParse[i][0] and word in dependencyParse[i][0]:
                parent = [int(dependencyParse[i][1].split('{')[1].split('}')[0].split(' ')[2]),
                          dependencyParse[i][1].split('{')[0], dependencyParse[i][0]]
                parentsWithRelation.append(parent)
                break

    return parentsWithRelation


def findChildren(dependencyParse, wordIndex, word):
    """
    word index assumed to be starting at 1
    the third parameter is needed because of the collapsed representation of the dependencies...

    :param dependencyParse:
    :param wordIndex:
    :param word:
    :return:
    """

    wordsWithIndices = ((int(item[2].split('{')[1].split('}')[0].split(' ')[2]), item[2].split('{')[0]) for item in
                        dependencyParse)
    wordsWithIndices = list(set(wordsWithIndices))
    wordsWithIndices = sorted(wordsWithIndices, key=lambda item: item[0])

    wordIndexPresentInTheList = False
    for item in wordsWithIndices:
        if item[0] == wordIndex:
            wordIndexPresentInTheList = True
            break

    childrenWithRelation = []

    if wordIndexPresentInTheList:
        # print True
        for item in dependencyParse:
            currentIndex = int(item[1].split('{')[1].split('}')[0].split(' ')[2])
            if currentIndex == wordIndex:
                childrenWithRelation.append(
                    [int(item[2].split('{')[1].split('}')[0].split(' ')[2]), item[2].split('{')[0], item[0]])
    else:
        # find the closest following word index which is in the list
        nextIndex = 0
        for i in range(len(wordsWithIndices)):
            if wordsWithIndices[i][0] > wordIndex:
                nextIndex = wordsWithIndices[i][0]
                break

        if nextIndex == 0:
            return []
        for i in range(len(dependencyParse)):
            if int(dependencyParse[i][2].split('{')[1].split('}')[0].split(' ')[2]) == nextIndex:
                pos = i
                break
        for i in range(pos, len(dependencyParse)):
            if '_' in dependencyParse[i][0] and word in dependencyParse[i][0]:
                child = [int(dependencyParse[i][2].split('{')[1].split('}')[0].split(' ')[2]),
                         dependencyParse[i][2].split('{')[0], dependencyParse[i][0]]
                childrenWithRelation.append(child)
                break

    return childrenWithRelation


nlp_server = StanfordNLP()

if __name__ == '__main__':
    # nlp_server = StanfordNLP()
    # output = nlp_server.parse("Four men died in an accident.")
    # parsed = parseText("Four men died in an accident.")

    # lemmatized = lemmatize(parsed)
    # pos_tagged = posTag(parsed)

    from python.src.traditional.pair_feature.word_alignment.aligner import *
    from python.src.traditional.pair_feature.word_alignment.similarity import *

    # sentences = ["Four men died in an accident.", "4 people are dead from a collision."]
    # parseText(sentences)
    sentence1 = "Four men died in an accident."
    # sentence1 = "Good afternoon!"
    sentence2 = "4 people are dead from a collision."
    # sentence2 = "Good morning!"

    alignments = align(sentence1, sentence2)
    print(alignments[0])
    a = alignment_similarity(alignments)
    b = verb_alignment_similarity(alignments, wn.ADJ)

    print(alignments[1])
