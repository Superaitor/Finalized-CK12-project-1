import pickle
import codecs
import glob
import gensim
from nltk import word_tokenize


#creates new word vector "pkl" file

files = glob.glob('/Users/superaitor/PycharmProjects/word2vecclassify/txtfiles/*.txt')
words = set()
for each_file in files:
    #print(each_file)
    with codecs.open(each_file, encoding='utf-8') as fd:
        txt_content = fd.read()
    words.update(word_tokenize(txt_content))

model = gensim.models.KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)

word_vectors = {}
for each_word in words:
    try:
        word_vectors[each_word] = model.get_vector(each_word)
    except KeyError:
        pass

fd = open('word_vectors.pkl', 'wb')
pickle.dump(word_vectors, fd)
fd.close()
