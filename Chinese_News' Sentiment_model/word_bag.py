#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# python3.6
# windows7 & pycharm

# original author: https://github.com/sunxiangguo/chinese_text_classification
# improve: ljzhou

# target: Create a word bag

from sklearn.datasets.base import Bunch
from sklearn.feature_extraction.text import TfidfVectorizer
from Tools import readfile, readbunchobj, writebunchobj

    # Remove stop words
def vector_space(stopword_path, bunch_path, space_path, train_tfidf_path=None):
    stpwrdlst = readfile(stopword_path).splitlines()    # stop words file read
    bunch = readbunchobj(bunch_path)
    tfidfspace = Bunch(target_name=bunch.target_name, label=bunch.label, filenames=bunch.filenames, tdm=[],
                       vocabulary={})
    
    # Build a word bag by using TF-IDF
    if train_tfidf_path is not None:
        trainbunch = readbunchobj(train_tfidf_path)
        tfidfspace.vocabulary = trainbunch.vocabulary
        vectorizer = TfidfVectorizer(stop_words=stpwrdlst, sublinear_tf=True, max_df=0.5,
                                     vocabulary=trainbunch.vocabulary)
        tfidfspace.tdm = vectorizer.fit_transform(bunch.contents)
    else:
        vectorizer = TfidfVectorizer(stop_words=stpwrdlst, sublinear_tf=True, max_df=0.5)
        tfidfspace.tdm = vectorizer.fit_transform(bunch.contents)
        tfidfspace.vocabulary = vectorizer.vocabulary_

    writebunchobj(space_path, tfidfspace)
    #print("TF-IDF finish")

    # word bag of train and test set
if __name__ == '__main__':
    stopword_path = "train_word_bag/hlt_stop_words.txt"    # Stop word file
    bunch_path = "train_word_bag/train_set.dat"    # Bunch path
    space_path = "train_word_bag/tfdifspace.dat"    # TF-IDF path
    vector_space(stopword_path, bunch_path, space_path)

    bunch_path = "test_word_bag/test_set.dat"    # Bunch path
    space_path = "test_word_bag/testspace.dat"    # Word bag path
    train_tfidf_path = "train_word_bag/tfdifspace.dat"    # TF-IDF path
    vector_space(stopword_path, bunch_path, space_path, train_tfidf_path)
