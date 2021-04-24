import nltk
from nltk import *


def assignment2a(br_tw, br_ts):
    print("2a:")
    print("There are {0} words.".format(len(br_tw)))
    print("There are {0} sentences.".format(len(br_ts)))


def assignment2b(br_tw):
    print("\n2b:")
    print("The 50th word is {0} and the POS-tag is {1}".format(br_tw[49][0], br_tw[49][1]))
    print("The 75th word is {0} and the POS-tag is {1}".format(br_tw[74][0], br_tw[74][1]))


def assignment2c(br_tw):
    pos_tags = []
    for i in br_tw:
        pos_tags.append(i[1])
    pos_set = set(pos_tags)
    print("\n2c:")
    print("There are {0} different POS tags in this Brown category".format(len(pos_set)))


def assignment2de(br_tw):
    word_count = []
    tag_count = []
    for word in br_tw:
        word_count.append(word[0])
        tag_count.append(word[1])
    counted_words = Counter(word_count)
    counted_tags = Counter(tag_count)
    print("\n2d:")
    print("The top 15 words are: {0}".format(dict(sorted(counted_words.items(), key=lambda item: item[1], reverse=True)[:15])))
    print("\n2e:")
    print("The top 15 tags are: {0}".format(dict(sorted(counted_tags.items(), key=lambda item: item[1], reverse=True)[:15])))


def assignment2f(br_ts):
    tag_count = []
    tag_count2 = []
    for word in br_ts[19]:
        tag_count.append(word[1])
    for word in br_ts[39]:
        tag_count2.append(word[1])
    counted_tags = Counter(tag_count)
    counted_tags2 = Counter(tag_count2)
    print("\n2f:")
    print("Most frequent POS tag(s) in the 20th sentence: {0}".format(sorted(counted_tags, key=counted_tags.get, reverse=True)))
    print("Most frequent POS tag(s) in the 40th sentence: {0}".format(sorted(counted_tags2, key=counted_tags2.get, reverse=True)[0]))


def assignment2gh(br_tw):
    adverb_list = []
    adjective_list = []
    for word in br_tw:
        if word[1] == "RB":
            adverb_list.append(word[0])
        if word[1] == "JJ":
            adjective_list.append(word[0])

    counted_adverbs = dict(Counter(adverb_list))
    counted_adjectives = dict(Counter(adjective_list))
    print("\n2g:")
    print("The most frequent adverb is: {0}".format(sorted(counted_adverbs, key=counted_adverbs.get, reverse=True)[0]))
    print("\n2h:")
    print("The most frequent adjective is: {0}".format(sorted(counted_adjectives, key=counted_adjectives.get, reverse=True)[0]))


def assignment2ij(br_tw):
    so_list = []
    for word in br_tw:
        if word[0] == "so":
            so_list.append(word[1])
    counted_so = dict(Counter(so_list))
    print("\n2i:")
    print("Which POS tags are most frequent for 'so': {0}".format(set(so_list)))
    print("\n2j:")
    print("The most frequent POS tag for 'so': {0}".format(sorted(counted_so, key=counted_so.get, reverse=True)[0]))


def assignment2k(br_ts):
    rb_list = []
    cs_list = []
    ql_list = []
    for sentence in br_ts:
        if ("so", "RB") in sentence:
            rb_list.append(sentence)
        if ("so", "CS") in sentence:
            cs_list.append(sentence)
        if ("so", "QL") in sentence:
            ql_list.append(sentence)
    print("\n2k:")
    print("An example sentence with 'so' with the POS tag 'RB': {0}".format(rb_list[0]))
    print("An example sentence with 'so' with the POS tag 'CS': {0}".format(cs_list[0]))
    print("An example sentence with 'so' with the POS tag 'QL': {0}".format(ql_list[0]))


def assignment2l(br_tw):
    pre_rb = []
    following_rb = []
    pre_cs = []
    following_cs = []
    pre_ql = []
    following_ql = []
    for i in range(len(br_tw)):
        if br_tw[i] == ("so", "RB"):
            pre_rb.append(br_tw[i-1])
            following_rb.append(br_tw[i+1])
        if br_tw[i] == ("so", "CS"):
            pre_cs.append(br_tw[i-1])
            following_cs.append(br_tw[i+1])
        if br_tw[i] == ("so", "QL"):
            pre_ql.append(br_tw[i-1])
            following_ql.append(br_tw[i+1])
    counted_pre_rb = Counter(pre_rb)
    counted_following_rb = Counter(following_rb)
    counted_pre_cs = Counter(pre_cs)
    counted_following_cs = Counter(following_cs)
    counted_pre_ql = Counter(pre_ql)
    counted_following_ql = Counter(following_ql)
    print("\n2l:")
    print("The most likely preceding POS tag to the word 'so' with POS tag 'RB': {0}".format(sorted(counted_pre_rb, key=counted_pre_rb.get, reverse=True)[0][1]))
    print("The most likely following POS tag to the word 'so' with POS tag 'RB': {0}".format(sorted(counted_following_rb, key=counted_following_rb.get, reverse=True)[0][1]))
    print("The most likely preceding POS tag to the word 'so' with POS tag 'CS': {0}".format(sorted(counted_pre_cs, key=counted_pre_cs.get, reverse=True)[0][1]))
    print("The most likely following POS tag to the word 'so' with POS tag 'CS': {0}".format(sorted(counted_following_cs, key=counted_following_cs.get, reverse=True)[0][1]))
    print("The most likely preceding POS tag to the word 'so' with POS tag 'QL': {0}".format(sorted(counted_pre_ql, key=counted_pre_ql.get, reverse=True)[0][1]))
    print("The most likely following POS tag to the word 'so' with POS tag 'QL': {0}".format(sorted(counted_following_ql, key=counted_following_ql.get, reverse=True)[0][1]))


def pos_tag(text):
    tokenized_text = nltk.word_tokenize(text)
    tagged_text = nltk.pos_tag(tokenized_text)
    print("\n3:")
    print("Our home made pos tagger (only the first 10 words to show that it works): {0}".format(tagged_text[:10]))
    return tagged_text


def collocation(tagged_text):
    tagged_pos = [pos[1] for pos in tagged_text]

    bigram_measures = nltk.collocations.BigramAssocMeasures()
    finder = BigramCollocationFinder.from_words(tagged_pos)

    top_pmi = finder.nbest(bigram_measures.pmi, 5)
    top_raw = finder.nbest(bigram_measures.raw_freq, 5)

    print("\n4:")
    print("We used PMI to rank the top 5 most significant bigrams")
    print("\n")
    print("These are the top 5 bigrams (using PMI): {0}".format(top_pmi))
    print("These are the top 5 bigrams with raw frequencies: {0}".format(top_raw))
    print("\n")
    print("They don't look interesting, nothing unexpected happened")
    print("When looking at the PMI and raw frequencies you can see that the PMI bigrams have a lot of punctuation whereas the raw frequencies do not have any punctuation")
    print("These bigrams could be used for search engines (to auto-fill queries) and to see the meaning of words (for example the meaning of 'so')")


def main():
    with open("holmes.txt", "r") as text_open:
        text = text_open.read()
    br_tw = nltk.corpus.brown.tagged_words(categories='mystery')
    br_ts = nltk.corpus.brown.tagged_sents(categories='mystery')
    assignment2a(br_tw, br_ts)
    assignment2b(br_tw)
    assignment2c(br_tw)
    assignment2de(br_tw)
    assignment2f(br_ts)
    assignment2gh(br_tw)
    assignment2ij(br_tw)
    assignment2k(br_ts)
    assignment2l(br_tw)
    tagged_text = pos_tag(text)
    collocation(tagged_text)


if __name__ == "__main__":
    main()
