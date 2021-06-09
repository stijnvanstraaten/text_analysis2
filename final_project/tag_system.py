import wikipediaapi as wa
import nltk
import sys
from itertools import combinations

def get_all_possibilities(noun_list, en_wiki):
    length = len(noun_list)
    existing_combinations = []
    for L in range(length, 0, -1):
        for subset in combinations(noun_list, L):
            joined_subset = " ".join(subset)
            if en_wiki.page(joined_subset).exists():
                existing_combinations.append(joined_subset)
    return existing_combinations


def getwikilink(text, en_wiki):
    tags = [
                            ('COU', {'federation', 'city', 'country', 'state', 'capital', 'democratic', 'population', 'continent', 'province', 'district', 'continent', 'America', 'Iraq', 'independence', 'kingdom', 'island', 'autonomous', 'agricultural', 'NATO', 'border', 'borders', 'empire', 'kingdoms', 'territory', 'nation', 'languages', 'republic'}),
                            ('PER', {'he', 'she', 'born', 'friend', 'childhood', 'child', 'his', 'her', 'minister', 'politician', 'death', "Saddam"}),
                            ('ORG', {'organization', 'organisation', 'union', 'founded', 'business', 'corporation', 'administration', 'ideology', 'community', 'government', 'group', 'party'}),
                            ('CIT', {'city', 'town', 'district', 'urban', 'population', 'capital', 'metropolitan', 'village', 'centre', 'suburbs', 'named', 'region', 'place', 'capital', 'cultural', 'commercial', 'regional'}),
                            ('ANI', {'aquatic vertebrate',  'saltwater fish', 'species', 'predator', 'mammal', 'fish', 'reptile', 'animal', 'herbivore', 'omnivore', 'carnivore'}),
                            ('NAT', {'island', 'lake', 'shore', 'mountain', 'sea', 'river', 'volcano', 'island'}),
                            ('SPO', {'sport', 'team', 'Olympic', 'points', 'championship', 'ball'})
            ]

    noun_list = []
    text = text.rstrip().split("\n")
    pos_off = []
    sentence_counter = 0
    full_text = ""
    for line2 in text:
        full_text += line2.split()[3] + " "
    sentences = nltk.sent_tokenize(full_text)

    for line in text:
        line = line.split()
        pos_off.append(line)
        if line[4] == "NN" or line[4] == "NNP" or line[4] == "NNPS" or line[4] == "NNS":
            noun_list.append(line[3])
        elif noun_list != []:
            existing_combination = get_all_possibilities(noun_list, en_wiki)
            for combi in existing_combination:
                synset = nltk.wsd.lesk(sentences[sentence_counter], combi, 'n')
                if synset is not None:
                    try:
                        disambiguated_word = synset.lemmas()[1].name()
                    except IndexError:
                        disambiguated_word = synset.lemmas()[0].name()
                    page = en_wiki.page(disambiguated_word)
                else:
                    page = en_wiki.page(combi)
                summary = nltk.word_tokenize(page.summary)
                score_dict = {}
                for tag in tags:
                    for word in summary:
                        if word in tag[1]:
                            if tag[0] in score_dict.keys():
                                score_dict[tag[0]] += 1
                            else:
                                score_dict[tag[0]] = 1
                score_list = []
                summary_len = len(summary)
                for tag_dict_keys in score_dict.keys():
                    score_list.append([tag_dict_keys, score_dict[tag_dict_keys]/summary_len])
                winning_score = ["NON", 0]
                for score in score_list:
                    if score[1] > 0.015 and score[1] > winning_score[1]:
                        winning_score = score
                if winning_score[0] != "NON":
                    for i in range(2, len(noun_list) + 2):
                        if pos_off[-i][3] in combi and len(pos_off[-i]) < 6:
                            pos_off[-i].append(winning_score[0])
                            pos_off[-i].append(page.fullurl)
            if line[3] == ".":
                sentence_counter += 1

            noun_list = []
    for line in pos_off:
        print(" ".join(line))



def main():
    with open(sys.argv[1], "r") as text_open:
        text = text_open.read()
    en_wiki = wa.Wikipedia("en")

    getwikilink(text, en_wiki)


if __name__ == "__main__":
    main()