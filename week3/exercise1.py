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

    hypernym_list = {Synset('act.n.02'): "act", Synset('animal.n.01'): "animal", Synset('artifact.n.01'): "artifact", Synset('attribute.n.01'): "attribute", Synset('body.n.01'): "body", Synset('body.n.08'): "body", Synset('cognition.n.01'): "cognition", Synset('communication.n.01'): "communication", Synset('event.n.01'): "event", Synset('feeling.n.01'): "feeling", Synset('food.n.01'): "food", Synset('group.n.01'): "group", Synset('location.n.01'): "location", Synset('motive.n.01'): "motive", Synset('object.n.01'): "natural object", Synset('phenomenon.n.01'): "natural phenomenon", Synset('person.n.01'): "person", Synset('plant.n.02'): "plant", Synset('possession.n.01'): "possession", Synset('quantity.n.01'): "quantity", Synset('process.n.01'): "process", Synset('relation'): "relation", Synset('state.n.02'): "state", Synset('shape.n.01'): "shape", Synset('substance.n.01'): "substance", Synset('time'): "time"}


def hypernym(synset):
    print(synset.hypernyms())
    hypernym(synset.hypernyms()[0])



def main():
    with open("ada_lovelace.txt", "r") as text_read:
        text = text_read.read()

    assignment1(text)



if __name__ == "__main__":
    main()