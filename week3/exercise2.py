# exercise1.py
# 26-04-2021
# Huub exel, Rutger van der Hart, Stijn van Straaten

from nltk.parse import CoreNLPParser

def NER(text):
    ner_tagger = CoreNLPParser(url='http://localhost:9000', tagtype='ner')
    tokenized_text = ner_tagger.tokenize(text)
    tagged_text = ner_tagger.tag(tokenized_text)
    print(tagged_text)
    person_list = []
    organization_list = []
    locations_list = []
    date_list = []
    misc_list = []
    for i in tagged_text:
        if i[1] == "PERSON":
            person_list.append(i[0])
        if i[1] == "ORGANIZATION":
            organization_list.append(i[0])
        if i[1] == "LOCATION":
            locations_list.append(i[0])
        if i[1] == "DATE":
            date_list.append(i[0])
        if i[1] == "MISC":
            misc_list.append(i[0])

    print("The text contains {0} people, namely: {1}".format(len(person_list), person_list))
    print("The text contains {0} organizations, namely: {1}".format(len(organization_list), organization_list))
    print("The text contains {0} locations, namely: {1}".format(len(locations_list), locations_list))
    print("The text contains {0} dates, namely: {1}".format(len(date_list), date_list))
    print("The text contains {0} miscs, namely: {1}".format(len(misc_list), misc_list))

def main():
    with open("ada_lovelace.txt", "r") as text_open:
        text = text_open.read()
    NER(text)


if __name__ == "__main__":
    main()