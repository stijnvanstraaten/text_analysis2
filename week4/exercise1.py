# exercise1.py
# 7-5-2021
# Huub exel, Rutger van der Hart, Stijn van Straaten

import nltk
import os


def looptag(directory):
    for filename in os.listdir(directory):
        with open(directory + filename + '/en.tok.off', "r") as text_open:
            text = text_open.read()
        text_split = text.split("\n")
        sentence_items = []

        for i in text_split:
            if i != '':
                sentence_items.append(i.split(" "))
        tag_items = []

        for i in range(len(sentence_items)):
            sentence_items[i].append(nltk.pos_tag([sentence_items[i][3]])[0][1])

        for sentence in sentence_items:
            tag_items.append(' '.join(sentence))

        tag_items = '\n'.join(tag_items)

        with open(directory + filename + '/en.tok.off' + '.pos', 'w') as text_write:
            text_write.write(tag_items)


def main():
    looptag('./p49/')
    looptag('./p50/')


if __name__ == "__main__":
    main()
