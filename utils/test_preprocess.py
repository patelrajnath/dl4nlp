#!/usr/bin/env python

import codecs
import gzip
import cPickle
import json

import numpy as np

def read_pretrained_embedding(words_vector_file):
    """
        words_vector_file: file containing the trained word embeddings
        Usage: Returns the word2index dictionary and embedding
    """
    word2idx = {}
    embedding = []
    fv = codecs.open(words_vector_file, 'r', 'utf-8')
    flog = codecs.open(words_vector_file+'.log_duplicates', 'w', 'utf-8')
    idx = 0
    for line in fv:
        words = line.split(' ', 1)
        w = words[0].strip()
        if w not in word2idx:
            embedding.append([float(i) for i in words[1].strip().split()])
            word2idx[words[0].strip()] = idx
            idx += 1
        else:
            flog.write(line)
    fv.close()
    flog.close()

    return word2idx, embedding

def word2index(fname, word2idx):

    """
	fname: the file name to be converted into idx representation
	word2idx: a mapping from word to ids

	Usage: returns processed data with words converted to ids
    """

    fin = codecs.open(fname, 'r', 'utf-8')
    data = []
    
    for line in fin:
        sent_idx = []
        words = line.split()
        for word in words:
            w = word.strip()
            if w in word2idx:
                sent_idx.append(word2idx[w])
            else:
                sent_idx.append(word2idx['UNK'])
        data.append(np.asarray(sent_idx))
        
    return data


def process_embedding(words_vector_file):
    """
	fname: the file name containing the text to be processed
	words_vector_file: pretrained word embedding from word2vec (text-model)

	Usage: Returns mapping of words2index and prepared data
    """
    word2idx , emb = read_pretrained_embedding(words_vector_file)
    ne = len(emb)
    de = len(emb[0])

    #For unknow words and padding
    word2idx['UNK'] = ne + 1
    word2idx['_padding'] = ne + 2
    #Add initial embedding for UNK and padding	
    emb.append([0] * de)
    emb.append([0] * de)

    return word2idx, emb

def get_aligned_src(data):

    """
	data: contains data_train, data_test, and data_valid
	data_train: train.src, train.mt, train.align; similarly for data_test and data_valid
    """
    new_data = []
    for d in data:
 	f_src = codecs.open(d[0], 'r', 'utf-8')
  	f_tgt = codecs.open(d[1], 'r' 'utf-8')
  	f_align = codecs.open(d[2], 'r', 'utf-8')
  	fout_src = codecs.open(d[0] + '.prep', 'w', 'utf-8')

  	fnames = [d[0]+ '.prep', d[1]]
 	new_data.append(fnames)

  	for s,t,a in zip(f_src, f_tgt, f_align):
     		s_words = s.split()
     		t_words = t.split()
     		a_idxs = a.split()
     		n = len(t_words)
     		sent = ''
     		for i in range(n):
        		flag = True
        		for aidx in a_idxs:
            			idxs = aidx.split('-')
            			sidx = int(idxs[0])
            			tidx = int(idxs[1])
            			if i == tidx:
                			flag = False
                			sent += s_words[sidx].strip() + ' '
                			break
        		if(flag):
            			sent += 'null' + ' '
     		fout_src.write(sent.strip()+'\n')

	f_src.close()
	f_tgt.close()
	f_align.close()
	fout_src.close()

    return new_data

def preprocess_data(data_test, data_test_y, dictionaries, label2index, embeddings=None,
			use_bilingual=False, use_pretrain=False):
	"""
		
	"""
	if use_bilingual:
		assert (len(data_test) == 3), \
			"source, target, and alignment must be provided when using --use_bilingual"
	if use_pretrain:
		assert embeddings, "word embedding must be provided when using --use_pretrain"
	if use_pretrain and use_bilingual:
		assert len(embeddings) == 2, "enbedding for both source and target must be provided when using --use_pretrain and --use_bilingual"
	
	#get the aligned src as per the alignment file and target
	if use_bilingual:
		data_sets = get_aligned_src([data_test])
		data_test = data_sets[0]

	#init empty lists for various data sets
	w2idxs, embs, test, test_y = ([] for i in range(4))

	if use_pretrain:
		for pretrain_emb in embeddings:
			w2idx, emb = process_embedding(pretrain_emb)
			w2idxs.append(w2idx)
			embs.append(emb)
	else:
		for _dict in dictionaries:
			w2idxs.append(json.load(open(_dict)))
			embs.append([])

	for tf, w2idx in zip(data_test, w2idxs):
    		test.append(word2index(tf, w2idx))

        label2idx = json.load(open(label2index))
    	test_y = word2index(data_test_y, label2idx)
	data = [test, test_y, w2idxs, label2idx, embs]
	return data

if  __name__ == '__main__':
	data = preprocess_data(
          data_test=['data/qe/test/test.src.lc',
		'data/qe/test/test.mt.lc',
		'data/qe/test/test.align'],
	  data_test_y = 'data/qe/test/test.tags',
          dictionaries=['data/qe/train/train.src.lc.json',
              'data/qe/train/train.mt.lc.json'],
	  embeddings=['data/qe/pretrain/ep_qe.en.vector.txt',
	      'data/qe/pretrain/ep_qe.de.vector.txt'],
	  label2idx = 'data/qe/train/train.tags.json')

	print data[0][0][0]