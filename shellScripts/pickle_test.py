import pickle
import bz2
import _pickle as cPickle


def compressed_pickle(title, data):
 with bz2.BZ2File(title + ‘.pbz2’, ‘w’) as f: 
 cPickle.dump(data, f)

#compressed_pickle('filename', data) 


infile = open('session.ebf','rb')
new_dict = pickle.load(infile)
print(new_dict)
infile.close()
