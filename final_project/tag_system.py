import wikipediaapi as wa                   # we found that this wikipedia api worked better than the one we got in class
import nltk
import sys
from itertools import combinations

def get_all_possibilities(noun_list, en_wiki):
    """
    This takes a serie with NN (or NNP, NNPS, NNS) words and splits them into every possible order.
    Example: you have the serie, 1 2 3 4     (I know these are not NN but it's just for the example)
    What this gives you is:
    1 2 3 4
    1 2 3
    1 2 4
    1 3 4
    2 3 4
    1 2
    1 3
    ....... and so on. It basically gives you every possibility of the serie.
    
    After this it checks if there exist a Wikipedia page for the existing combination and if so,
    it will add that to the existing_combinations list and return that.
    """
    
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
                            ('NAT', {'island', 'lake', 'shore', 'mountain', 'sea', 'river', 'volcano'}),
                            ('SPO', {'sport', 'team', 'Olympic', 'points', 'championship', 'ball'})
            ]
    
    noun_list = []                      # All the nouns that are in the text will end up in here
    text = text.rstrip().split("\n")
    pos_off = []                        # This is where the endresult will be put in
    
    # These two lines are used by Lesk
    sentence_counter = 0
    full_text = ""
    
    # this part is build so that Lesk can read the whole sentence
    for line2 in text:
        full_text += line2.split()[3] + " "
    sentences = nltk.sent_tokenize(full_text)

    for line in text:
        line = line.split()
        pos_off.append(line)
        
        # If the tag behind the word is either NN, NNP, NNPS or NNS, append it to the noun_list
        if line[4] == "NN" or line[4] == "NNP" or line[4] == "NNPS" or line[4] == "NNS":
            noun_list.append(line[3])
            
        elif noun_list != []:
            # get all the existing combinations for a serie
            existing_combination = get_all_possibilities(noun_list, en_wiki)
            for combi in existing_combination:
                synset = nltk.wsd.lesk(sentences[sentence_counter], combi, 'n')
                # there is no synset for most persons so you cannot get a synset for those 
                if synset is not None:
                    try:
                        # if there is a more clear synonym for that word, use that.
                        disambiguated_word = synset.lemmas()[1].name()
                    except IndexError:
                        # if the word does not really have a more clear synonym, use the word itself.
                        disambiguated_word = synset.lemmas()[0].name()
                    page = en_wiki.page(disambiguated_word)
                else:
                    page = en_wiki.page(combi)
                    
                summary = nltk.word_tokenize(page.summary) # get the wikipedia summary of the word.
                
                # This keeps track of the amount of tags that are found in the summary of the word and
                # it does this for each of the 7 categories seperate.
                score_dict = {}
                
                # if one of the words in the summary is in one of the 7 "tags" (categories) it does +1
                # for that category in the score_dict
                for tag in tags:
                    for word in summary:
                        if word in tag[1]:
                            if tag[0] in score_dict.keys():
                                score_dict[tag[0]] += 1
                            else:
                                # if this is the first +1 for that category (for this word) it adds
                                # the category and sets the score to 1
                                score_dict[tag[0]] = 1
                                
                # for every category calculate what percentage of the page is used for that category               
                score_list = [] 
                for tag_dict_keys in score_dict.keys():
                    score_list.append([tag_dict_keys, score_dict[tag_dict_keys]/len(summary)])
                
                winning_score = ["NON", 0] # set the winning score to "NON", 0 so we can compare it below here
                for score in score_list:
                    # 0.015% is the benchmark to prove that it is even valid enough to be categorised as 1 of the 7
                    if score[1] > 0.015 and score[1] > winning_score[1]:
                        winning_score = score # highest score becomes the winning score
                if winning_score[0] != "NON": # check if the benchmark is met atleast once.
                    for i in range(2, len(noun_list) + 2):
                        if pos_off[-i][3] in combi and len(pos_off[-i]) < 6:
                            pos_off[-i].append(winning_score[0])
                            pos_off[-i].append(page.fullurl)
                            
            # This is to easily count the sentences for Lesk                
            if line[3] == ".":
                sentence_counter += 1

            noun_list = []
            
    # prints every line to the file        
    for line in pos_off:
        print(" ".join(line))



def main():
    # The system works with argv so you can use the terminal to put a file in that you want the system to work on.
    # tag_system.py /home/stijn/textanalysis/final_roject/dev/p16/d0455/en.tok.pos.off > file_you_want_the_result_in
    # The line above this one shows what we put in the terminal to make it work.
    with open(sys.argv[1], "r") as text_open:
        text = text_open.read()
        
    # This line makes sure that we get the english Wikipedia page of that what we are searching    
    en_wiki = wa.Wikipedia("en")                

    # The big function where the magic happens.
    getwikilink(text, en_wiki)


if __name__ == "__main__":
    main()
