# exercise1.py
# 26-04-2021
# Huub exel, Rutger van der Hart, Stijn van Straaten

import nltk
from nltk.corpus import wordnet
from nltk.stem.wordnet import WordNetLemmatizer

def hypernymOf(synset1, synset2):
    if synset1 == synset2:
        return True
    for hypernym in synset1.hypernyms():
        if synset2 == hypernym:
            return True
        if hypernymOf(hypernym, synset2):
            return True
    return False


def assignment1(text):
    tokenized_text = nltk.word_tokenize(text)
    pos_text = nltk.pos_tag(tokenized_text)
    nouns = []
    noun_lemmas = []

    for word in pos_text:
        if word[1] == "NN":
            nouns.append(word[0])

    lemmatizer = WordNetLemmatizer()

    for noun in nouns:
        noun_lemmas.append(lemmatizer.lemmatize(noun, wordnet.NOUN))

    relative = wordnet.synsets("relative", pos="n")[0]
    illness = wordnet.synsets("illness", pos="n")[0]
    science = wordnet.synsets("science", pos="n")[0]

    relative_nouns = []
    illness_nouns = []
    science_nouns = []
    for noun in noun_lemmas:
        synset1 = wordnet.synsets(noun, pos="n")
        if type(synset1) is list:
            check_relative = 0
            check_illness = 0
            check_science = 0
            for item in synset1:
                if hypernymOf(item, relative) and check_relative == 0:
                    relative_nouns.append(noun)
                    check_relative = 1
                if hypernymOf(item, illness) and check_illness == 0:
                    illness_nouns.append(noun)
                    check_illness = 1
                if hypernymOf(item, science) and check_science == 0:
                    science_nouns.append(noun)
                    check_science = 1
        else:
            if hypernymOf(synset1, relative):
                relative_nouns.append(noun)
            if hypernymOf(synset1, illness):
                illness_nouns.append(noun)
            if hypernymOf(synset1, science):
                science_nouns.append(noun)

    print("1a:")
    print("There are {0} nouns that refer to a relative, they are:\n{1}".format(len(relative_nouns), relative_nouns))
    print("\n1b:")
    print("There are {0} nouns that refer to a illness, they are:\n{1}".format(len(illness_nouns), illness_nouns))
    print("\n1c:")
    print("There are {0} nouns that refer to a science, they are:\n{1}".format(len(science_nouns), science_nouns))

    hypernym_dict = {wordnet.synsets("act", pos="n")[1]: "act", wordnet.synsets("animal", pos="n")[0]: "animal", wordnet.synsets('artifact', pos="n")[0]: "artifact", wordnet.synsets('attribute', pos="n")[0]: "attribute", wordnet.synsets('body', pos="n")[0]: "body", wordnet.synsets('body', pos="n")[7]: "body", wordnet.synsets('cognition', pos="n")[0]: "cognition", wordnet.synsets('communication', pos="n")[0]: "communication", wordnet.synsets('event', pos="n")[0]: "event", wordnet.synsets('feeling', pos="n")[0]: "feeling", wordnet.synsets('food', pos="n")[0]: "food", wordnet.synsets('group', pos="n")[0]: "group", wordnet.synsets('location', pos="n")[0]: "location", wordnet.synsets('motive', pos="n")[0]: "motive", wordnet.synsets('object', pos="n")[0]: "natural object", wordnet.synsets('phenomenon', pos="n")[0]: "natural phenomenon", wordnet.synsets('person', pos="n")[0]: "person", wordnet.synsets('plant', pos="n")[1]: "plant", wordnet.synsets('possession', pos="n")[0]: "possession", wordnet.synsets('quantity', pos="n")[0]: "quantity", wordnet.synsets('process', pos="n")[0]: "process", wordnet.synsets('relation', pos="n")[0]: "relation", wordnet.synsets('state', pos="n")[1]: "state", wordnet.synsets('shape', pos="n")[0]: "shape", wordnet.synsets('substance', pos="n")[0]: "substance", wordnet.synsets('time', pos="n")[0]: "time"}
    final_list = []

    for noun in noun_lemmas:
        noun_synset_set = set()
        synset1 = wordnet.synsets(noun, pos="n")

        if synset1:
            for i in synset1:
                hypernym(i, hypernym_dict, noun_synset_set)
            final_list.append([noun, noun_synset_set])

    noun_one = []
    noun_more = []
    total_length = 0

    for item in final_list:
        if len(item[1]) == 1:
            noun_one.append(item)
        if len(item[1]) > 1:
            noun_more.append(item)
        total_length += len(item[1])

    print("\n2:")
    print("There were {0} cases of a noun only having one hypernym, for example:\n{1}".format(len(noun_one), noun_one[:3]))
    print("\nThere were {0} cases where we had to choose between multiple hypernyms. Our system did not make any choice, we just followed all paths to the top hypernyms.\nTo make a decision you have to look at the context and make a decision for yourself, here are two examples:\n{1}".format(len(noun_more), noun_more[:2]))
    print("\nThe average length of hypernyms per noun is: {0}".format(total_length / len(final_list)))

    nounsynsets = [[wordnet.synsets("car", pos="n"), wordnet.synsets("automobile", pos="n")], [wordnet.synsets("coast", pos="n"), wordnet.synsets("shore", pos="n")], [wordnet.synsets("food", pos="n"), wordnet.synsets("fruit", pos="n")], [wordnet.synsets("journey", pos="n"), wordnet.synsets("car", pos="n")], [wordnet.synsets("monk", pos="n"), wordnet.synsets("slave", pos="n")], [wordnet.synsets("moon", pos="n"), wordnet.synsets("string", pos="n")]]
    words = ["car<>automobile", "coast<>shore", "food<>fruit", "journey<>car", "monk<>slave", "moon<>string"]
    scores = {}
    index = 0

    for nounsynset in nounsynsets:
        scores[words[index]] = getMaxSim(nounsynset[0], nounsynset[1])
        index += 1

    print("\n3:")
    for i in sorted(scores.items(), key=lambda item: item[1], reverse=True):
        print("{0}\t\t{1}".format(i[0], i[1]))


def getMaxSim(synset1, synset2):
    maxSim = None
    for s1 in synset1:
        for s2 in synset2:
            sim = s1.lch_similarity(s2)
            if maxSim is None or maxSim < sim:
                maxSim = sim
    return maxSim


def hypernym(synset, hypernym_dict, noun_synset_set):
    if synset in hypernym_dict.keys():
        noun_synset_set.add(synset)
    synset_hypernym = synset.hypernyms()
    if synset_hypernym:
        for syn_hypernym in synset_hypernym:
            hypernym(syn_hypernym, hypernym_dict, noun_synset_set)






def main():
    with open("ada_lovelace.txt", "r") as text_read:
        text = text_read.read()

    assignment1(text)



if __name__ == "__main__":
    main()