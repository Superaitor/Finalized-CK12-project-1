import pickle
import codecs
import glob
from nltk import word_tokenize

#creates the word similarities list

files = glob.glob('/Users/superaitor/PycharmProjects/word2vecclassify/txtfiles/*.txt')
words = set()
for each_file in files:
    #print(each_file)
    with codecs.open(each_file, encoding='utf-8') as fd:
        txt_content = fd.read()
    words.update(word_tokenize(txt_content))


fd = open('word_similarities.pkl', 'wb')
pickle.dump(words, fd)
fd.close()
