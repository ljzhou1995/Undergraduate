#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# python3.6
# windows7 & pycharm

# original author: https://github.com/sunxiangguo/chinese_text_classification
# improve: ljzhou

# target: Chinese text(financial news) segment


import os
import jieba
from Tools import savefile, readfile


# corpus_path is the unsegmented corpus path
# seg_path is the segmented corpus path
def corpus_segment(corpus_path, seg_path):   
    catelist = os.listdir(corpus_path)  # Gets all subdirectories under corpus_path
    ## In fact, the name of subdirectories is the category
    #print("Segmenting..Please wait.")
    
    # Gets all the files under each directory (category)
    for mydir in catelist:
        class_path = corpus_path + mydir + "/"
        seg_dir = seg_path + mydir + "/"
        if not os.path.exists(seg_dir):  # Whether there is a word segmentation directory, if not, create it
            os.makedirs(seg_dir)
        file_list = os.listdir(class_path)  # Get all the text in a category in an unsegmented term repository
            
    # Traverse all files in the category directory and to process
        for file_path in file_list:
            fullname = class_path + file_path
            content = readfile(fullname)
            content = content.replace('\r\n'.encode('utf-8'), ''.encode('utf-8')).strip()  # Delete line breaks
            content = content.replace(' '.encode('utf-8'), ''.encode('utf-8')).strip()  # Delete empty lines, extra spaces
            content_seg = jieba.cut(content)  # segment
            savefile(seg_dir + file_path, ' '.join(content_seg).encode('utf-8'))  # Save the segmented file
    #print("Finish.")

    # Segmentation of train and test sets.
if __name__ == "__main__":
    corpus_path = "./train_corpus/"  # Unsegmented
    seg_path = "./train_corpus_seg/"  # Segmented
    corpus_segment(corpus_path, seg_path)
    
    corpus_path = "./test_corpus/"  # Unsegmented
    seg_path = "./test_corpus_seg/"  # Segmented
    corpus_segment(corpus_path, seg_path)
