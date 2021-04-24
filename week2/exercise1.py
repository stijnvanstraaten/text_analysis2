# exercise1.py
# 19-04-2021
# Huub exel, Rutger van der Hart, Stijn van Straaten

import nltk
from nltk.collocations import *


def chi(bigram_measures, find):
    for item in find.nbest(bigram_measures.chi_sq, 20):
        print(item)


def pmi(bigram_measures, find):
    for item in find.nbest(bigram_measures.pmi, 20):
        print(item)


def raw_freq(bigram_measures, find):
    for item in find.nbest(bigram_measures.raw_freq, 20):
        print(item)


def main():
    with open("holmes.txt", "r") as text_read:
        text = text_read.read()

    tokenizer = nltk.RegexpTokenizer(r"\w+")
    tokenized_text = tokenizer.tokenize(text)

    bigram_measures = nltk.collocations.BigramAssocMeasures()
    find = BigramCollocationFinder.from_words(tokenized_text)
    # You could use the following line to reduce ambiguity, by 
    # removing bigrams with a frequency lower than 3.
    #find.apply_freq_filter(3)
    print("Exercise 1.1:")
    print("\na:")
    pmi(bigram_measures, find)
    print("\nb:")
    chi(bigram_measures, find)
    print("\nc:")
    raw_freq(bigram_measures, find)

if __name__ == "__main__":
    main()
