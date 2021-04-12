import nltk
import collections


def Average(lst):
    """This function calculates the average"""
    return sum(lst) / len(lst)


def exercise1(tokenized_sentences):
    """This function gets the longest sentence, the shortest sentence,
    the distributions of sentences in terms of length and the average sentence length"""
    tokenized_words = []
    lengths = []
    max = [0, ""]
    min = [1000, ""]
    # These exceptions prevent that abbreviations/non-sentences get seen as sentences
    exceptions = ["I.", "II.", "III.", "IV.", "V.", "VI.", "VII.", "VIII.", "IX.", "X.", "XI.", "XII.", "K.", "4.",
                  "4.'", "O.\"", "4d.", "B.\"", "B.'"]
    for sentence in tokenized_sentences:
        if sentence not in exceptions:
            tokenized_words.append(nltk.word_tokenize(sentence))
    for sentence in tokenized_words:
        lengths.append(len(sentence))
        if len(sentence) > max[0]:
            max = [len(sentence), ' '.join(sentence)]
        elif len(sentence) == max[0]:
            max.append(' '.join(sentence))
        if len(sentence) < min[0]:
            min = [len(sentence), ' '.join(sentence)]
        elif len(sentence) == min[0]:
            min.append(' '.join(sentence))

    frequencies_lengths = collections.Counter(lengths)
    sorted_frequencies_lengths = sorted(frequencies_lengths.items(), key=lambda item: item[0])

    print("1a: The longest sentence is {0} words long: {1}\n".format(max[0], max[1]))
    print("1b: The shortest sentence is {0} words long: {1}\n".format(min[0], min[1:]))
    print("1c: A list with the length of sentences with their frequencies in this format: (length, frequency)\n{0}\n".format(sorted_frequencies_lengths))
    print("1d: The average sentence length in the whole document: {0}\n".format(round(Average(lengths), 2)))


def ngram(text, N):
    """This function returns the top 20 ngrams depending on type with descending frequency"""
    ngram_list = nltk.ngrams(text, N)
    ngram_list = collections.Counter(ngram_list)
    return sorted(ngram_list.items(), key=lambda item: item[1], reverse=True)[:20]


def exercise2(tokenized_sentences, tokenized_words, text):
    """This function makes exercise 2"""
    characters = []
    for sentence in tokenized_sentences:
        for character in sentence:
            characters.append(character)
    set_characters = set(characters)
    print("2a: The number of character types is {0} followed by the character type list alphabetically ordered: {1}".format(len(set_characters), sorted(set_characters)))

    words = []
    for word in tokenized_words:
        words.append(word)
    set_words = set(words)
    print("\n2b: The number of token types is {0} followed by the token type list alphabetically ordered: {1}".format(len(set_words), sorted(set_words)))

    print("\n2c: Here are the top 20 character-level unigrams, bigrams and trigrams ordered by descending frequency")
    print(ngram(text, 1))
    print(ngram(text, 2))
    print(ngram(text, 3))

    print("\n2d: Here are the top 20 token-level unigrams, bigrams and trigrams ordered by descending frequency")
    print(ngram(tokenized_words, 1))
    print(ngram(tokenized_words, 2))
    print(ngram(tokenized_words, 3))


def main():
    with open("holmes.txt", "r") as text_open:
        text = text_open.read()
    tokenized_sentences = nltk.sent_tokenize(text)
    tokenized_words = nltk.word_tokenize(text)
    exercise1(tokenized_sentences)
    exercise2(tokenized_sentences, tokenized_words, text)


if __name__ == "__main__":
    main()
