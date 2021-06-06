import wikipediaapi as wa
import nltk
import sys

def getwikilink(text):
    en_wiki = wa.Wikipedia("en")
    tags = [
                            ('COU', {'country', 'state', 'population', 'continent', 'province', 'kingdom', 'European', 'Asian', 'sovereign', 'independence', 'district'}),
                            ('PER', {'he', 'she', 'born', 'child', 'siblings', 'friend'}),
                            ('ORG', {'organization', 'organisation', 'union', 'founded', 'business', 'corporation', 'administration', 'ideology'}),
                            ('CIT', {'national capital', 'city', 'capital', 'town', 'Capital', 'population', 'district'}),
                            ('ANI', {'aquatic vertebrate',  'saltwater fish', 'species', 'predator', 'mammal', 'fish', 'reptile', 'animal', 'herbivore', 'omnivore', 'carnivore'}),
                            ('NAT', {'island', 'lake', 'shore', 'mountain', 'sea', 'river', 'volcano'}),
                            ('SPO', {'sport', 'team', 'Olympic', 'points', 'championship', 'ball'})
            ]

    noun_list = []
    text = text.rstrip().split("\n")
    for line in text:
        line = line.split()
        if line[4] == "NN" or line[4] == "NNP" or line[4] == "NNPS" or line[4] == "NNS":
            noun_list.append(line[3])
        elif noun_list != []:
            wiki_word = " ".join(noun_list)
            if en_wiki.page(wiki_word).exists():
                page = en_wiki.page(wiki_word)
                summary = set(nltk.word_tokenize(page.summary))
                summary_len = len(nltk.word_tokenize(page.summary))
                score_list = []
                for tag in tags:
                    len_intersection = len(tag[1].intersection(summary))
                    #print(tags[2][1].intersection(set(nltk.word_tokenize(en_wiki.page("militants").summary))))
                    if len_intersection > 0:
                        score_list.append([tag[0], len_intersection / len(tag[1])])
                print("{0}\n{1}\n{2}\n".format(wiki_word, score_list, summary_len))
            noun_list = []



def main():
    with open(sys.argv[1], "r") as text_open:
        text = text_open.read()

    getwikilink(text)


if __name__ == "__main__":
    main()