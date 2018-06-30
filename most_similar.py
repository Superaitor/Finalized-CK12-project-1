# from word_2_vec import cleanup
import pickle
from scipy.spatial.distance import cosine
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from nltk import pos_tag


def main3(word):
    # main()
    k = word
    fd = open('word_similarities.pkl', 'rb')
    things = pickle.load(fd)
    words = cleanup(things)
    neighbors = nearest_neighbors(k, words)
    return neighbors


def cleanup(file):
    x = list()
    stop_words = set(stopwords.words('ck12stopwords'))
    for words in file:
        if (not len(words) < 3 and '-' not in words and '=' not in words
                and '/' not in words and '.' not in words and '%' not in words
                and words not in stop_words):
            x.append(words)
    return x


def noun_finder(file):
    x = list()
    for words in file:
        if words[1] == "NN" or words[1] == "NNP" or words[1] == "NNS":
            x.append(words[0])
    return x


def nearest_neighbors(k, files):
    stemmer = SnowballStemmer("english")
    fd = open('word_vectors.pkl', 'rb')
    word_vectors = pickle.load(fd)
    total_similarities = {}
    numbers = []
    neighbors = []
    stemmed = list()
    all = pos_tag(word_vectors)
    nouns = list()
    for words in all:
        if words[1] == "NN" or words[1] == "NNP":
            nouns.append(words[0])
    for words in nouns:
        try:
            total_similarities.update({(1 - cosine(word_vectors[words], word_vectors[k])): words})
            numbers.append(1 - cosine(word_vectors[words], word_vectors[k]))
        except KeyError:
            pass

    numbers.sort(reverse=True)
    n = 0
    while n < 4:
        try:
            if stemmer.stem(total_similarities[numbers[n + 10]].lower()) == stemmer.stem(k.lower()) or k.lower() in \
                    total_similarities[numbers[n + 10]].lower():
                neighbors.append(total_similarities[numbers[n + 20]])
                n += 1
                # continue
            for words in neighbors:
                if stemmer.stem(total_similarities[numbers[n + 10]].lower()) == stemmer.stem(
                        words.lower()) or words.lower() in total_similarities[numbers[n + 10]].lower():
                    neighbors.append(total_similarities[numbers[n + 20]])
            else:
                neighbors.append(total_similarities[numbers[n + 10]])
                n += 1
        except KeyError:
            pass
    return neighbors

