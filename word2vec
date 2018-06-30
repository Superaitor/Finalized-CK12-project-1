import csv
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
import gensim, logging
from scipy.spatial.distance import cosine
from gensim import corpora
import six
import os
import pickle
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import enchant

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


def main(s, link):
    # s = input("enter link of text you want to find key words of: ")
    # f = open(s, "r")
    text = word_tokenize(s)
    keys = keywords(link)
    tags = nltk.pos_tag(text)
    clean = cleanup(tags)
    yr = year_recognizer(clean)
    nouns = noun_finder(clean)
    ent = entity_recognizer(clean)
    split = array_splitter(nouns)
    m = lda(split)
    topics = topic_sorter(m)
    u = word2vec(nouns, topics, keys, yr, ent)
    # printer(u)
    return u


def cleanup(file):  # cleans up the text, getting rid of symbols that may negatively affect the code and add no meaning
    x = list()
    y = list()
    stop_words = set(stopwords.words('ck12stopwords'))
    for words in file:
        if (not len(words[0]) < 3 and '-' not in words[0] and ' ' not in words[0]
                and '/' not in words[0] and '.' not in words[0] and '%' not in words[0]
                and words[0] not in stop_words):
            x.append(words[0])
            y.append(words[1])
    z = list(zip(x, y))
    return z


def year_recognizer(file):  # Recognizes numbers from 100 to 2500, which in most of the cases, will be years.
    repeats = list()
    years = list()
    for words in file:
        if words[0].isdigit() and words[0] not in repeats:
            if int(words[0]) > 100 or int(words[0]) < 2500:
                repeats.append(words[0])
                years.append(words[0])
    return years


def noun_finder(file):  # finds nouns (or potentially other POS if added to code)
    x = list()
    for words in file:
        if words[1] == "NN" or words[1] == "NNP" or words[1] == "NNS":
            x.append(words[0])
    return x


def array_splitter(file):  # splits the entire list of words into groups of 5, which is done so these groups can be
    # treated as separate documents that LDA can run through (LDA requires more than one document,
    # and since there is only one document being inputed, I split that document into groups)
    size = len(file)
    dubs = []
    adder = []
    i, m, n = 0, 0, 0
    while size > m:

        while i + 5 > m:
            if size > m:
                f = file[m]
                adder.append(f)
                m += 1
            else:
                break
        i = m
        n += 1
        dubs.append(adder)
        adder = []

    return dubs


def lda(file):  # Runs LDA, finding the best topics most closely related to the text
    dictionary = corpora.Dictionary(file)
    corpus = [dictionary.doc2bow(text) for text in file]
    l_d_a = gensim.models.ldamodel.LdaModel
    ldamodel = l_d_a(corpus, num_topics=1, id2word=dictionary, passes=50)
    topics = ldamodel.print_topics(num_topics=1, num_words=3)
    return topics


def topic_sorter(topics):  # Extracts the LDA topics into a list
    splitter = ""
    ind = 0
    tops = []
    separate_words = ""
    odds = 0
    indexes = []
    x = 0
    i = 0
    for word in topics:
        splitter += str(word[1])
    while x < 3:
        if splitter[ind] is '"':
            odds += 1
            if odds % 2 == 1:
                indexes.append(ind)
                x += 1
        ind += 1
    while i < 3:
        for let in splitter[indexes[i] + 1:]:
            if let != '"':
                separate_words += let
            else:
                break
        tops.append(separate_words)
        i += 1
        separate_words = ""

    return tops


def word2vec(file, topic, key, years, ents):  # Returns the most similar words to the topics found by LDA
    x = list()
    repeats = list()
    n = 0
    total_similarities = list()

    fd = open('word_vectors.pkl', 'rb')
    word_vectors = pickle.load(fd)

    while n < len(topic):
        i = 0
        repeats = list()
        for words in file:
            if words.lower() not in repeats and words in word_vectors:
                repeats.append(words.lower())
                if n == 0:
                    total_similarities.append(1 - cosine(word_vectors[words], word_vectors[topic[n]]))
                else:
                    total_similarities[i] += cosine(1 - word_vectors[words], word_vectors[topic[n]])
                    # print(cosine(1 - word_vectors[words], word_vectors[topic[n]]))
                i += 1

        n += 1
    for s in total_similarities:
        s /= len(topic)

    for w in key:
        topic.append(w)

    check = 2.5
    while len(x) <= 5 or len(x) > 10:
        i = 0
        repeats = list()
        x = list()
        for words in file:
            if words.lower() not in repeats and words in word_vectors:
                repeats.append(words.lower())
                if total_similarities[i] >= check or words in key:
                    x.append(words)
                i += 1
        if len(x) <= 5:
            check -= 0.01
        if len(x) > 10:
            check += 0.01



    for numbers in years:
        x.append(numbers)
    for entities in ents:
        x.append(entities[0])
    return x


def tester():  # Just a tester for word2vec, ignore
    model = gensim.models.KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)
    x = model.similarity('Pharmacogenomics', 'polymerase')
    print(x)


def keywords(file_name):  # from the ck12 database, finds the lesson number being used, and extracts the lesson topic(s)
    # associated with that lesson, adding those to the topics found by LDA
    array = list()
    multiplier = 1
    name = str(file_name)
    lgth = len(name)
    number = 0
    x = lgth - 5
    keys = list()
    while str(9) >= name[x] >= str(0):
        number += (int(name[x]) * multiplier)
        x -= 1
        multiplier *= 10
    with open('artifact_vocabularies.csv', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            array.append(row)
    for key in array:
        if key[0] == str(number) and " " not in key[1]:
            keys.append(key[1])
    return keys


def entity_recognizer(clean):  # Recognizes Entities, specifically names of people and places, to be added into the
    # question making process
    text = ""
    for words in clean:
        text += words[0] + " "

    # text = " ".join(nouns)
    d = enchant.Dict("en_US")
    #  fd = open('word_vectors.pkl', 'rb')
    # word_vectors = pickle.load(fd)

    os.environ[
        "GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/superaitor/PycharmProjects/word2vecclassify/CK12Project-481abd45da43.json"

    client = language.LanguageServiceClient()

    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')

    # Instantiates a plain text document.
    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)

    # Detects entities in the document. You can also analyze HTML with:
    #   document.type == enums.Document.Type.HTML
    entities = client.analyze_entities(document).entities

    # entity types from enums.Entity.Type
    entity_type = ('UNKNOWN', 'PERSON', 'LOCATION', 'ORGANIZATION',
                   'EVENT', 'WORK_OF_ART', 'CONSUMER_GOOD', 'OTHER')
    categories = list()
    for entity in entities:
        cats = list()
        if (entity_type[entity.type] == "PERSON" or entity_type[entity.type] == "LOCATION") and "-" not in entity.name:
            # if entity.name.lower() not in word_vectors:
            if d.check(entity.name.lower()) is False:
                cats.append(entity.name)
                cats.append(entity_type[entity.type])
                # print(u'{:<16}: {}'.format('name', entity.name))
                # print(u'{:<16}: {}'.format('type', entity_type[entity.type]))
                categories.append(cats)
    better_categories = list()
    for words in categories:
        vocab = ""
        for let in words[0]:
            if let != " ":
                vocab += let
            else:
                break
        if d.check(vocab.lower()) is False:
            better_categories.append(words)

    return better_categories


def printer(file):  # if only finding key words, this can be used (with tweaked code) to print those keywords
    for words in file:
        print(words)

# main()

