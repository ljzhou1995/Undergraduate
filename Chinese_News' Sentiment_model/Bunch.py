#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# python3.6
# windows7 & pycharm

# original author: https://github.com/sunxiangguo/chinese_text_classification
# improve: ljzhou

# target: Create a Bunch

import os
import pickle

from sklearn.datasets.base import Bunch
from Tools import readfile

    # Create a Bunch
def corpus2Bunch(wordbag_path, seg_path):
    catelist = os.listdir(seg_path)
    bunch = Bunch(target_name=[], label=[], filenames=[], contents=[])
    bunch.target_name.extend(catelist)    # Expand the original list with the new list (addlist)
    
    # Add an element to the original list
    for mydir in catelist:
        class_path = seg_path + mydir + "/"
        file_list = os.listdir(class_path)
        for file_path in file_list:
            fullname = class_path + file_path
            bunch.label.append(mydir)
            bunch.filenames.append(fullname)
            bunch.contents.append(readfile(fullname))

    # Store bunch in wordbag_path
    with open(wordbag_path, "wb") as file_obj:
        pickle.dump(bunch, file_obj)
    #print("Bunch Finish")

    # Bunch of train and test set.
if __name__ == "__main__":
    wordbag_path = "train_word_bag/train_set.dat"  # Bunch path
    seg_path = "train_corpus_seg/"  # segmented corpus path
    corpus2Bunch(wordbag_path, seg_path)

    wordbag_path = "test_word_bag/test_set.dat"  # Bunch path
    seg_path = "test_corpus_seg/"  # segmented corpus path
    corpus2Bunch(wordbag_path, seg_path)
