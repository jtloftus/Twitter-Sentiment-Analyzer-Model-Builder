#!/usr/bin/env python

'''
Created on Nov 11, 2013
@author: Joe Loftus
'''

import re
from twitter_tokenizer import Tokenizer
import operator
from plistlib import writePlist

# Defines a dictionary of emoticons that consist of alpha characters that wouldn't be
# Completely stripped from the Text
letter_emoticons = {">:P", ":-P", ":P", "X-P", 'x-p', 'xp', 'XP', ':-p', ':p', '=p', \
                    ':-b', ':b', ':S', ':-X' ':X', ';D', \
                    '>:O', ':-O', ':O', 'D:<', 'D:', 'D8', 'D;', 'D=', 'DX', \
                    'v.v', 'D-:', ':-c', ':c', ':-D', ':D', '8-D', '8D', 'x-D', 'xD',\
                    'X-D', 'XD', '=-D', '=D', 'B^D', ':o)', ':c)', 'O:-)', '=:o]'}

# Generates a dictionary of Stopwords used to filter out words that hinder
# our ability to determine sentiment
def read_stopwords(filename):
    stopword_file = open(filename, 'r')   # open the file for reading
    stopwords = []
    for line in stopword_file:
        stopwords = line.split(",")
    stopword_file.close()
     
    dictionary = {}
    
    for word in stopwords:
        dictionary[word.strip()] = True
        
    return dictionary

# Removes Nonalpha characters
def format_string(s):
    return re.sub("[\W\d]+", "", s.strip())

# Function used to take twitter data pulled from
# iPhone print statements and generate a large text
# file populated by tweets on each line
def strip_nslog(filename):
    nslog_start = "2013-11-23"
    nslog_end = "70b]"
    
    T = Tokenizer(False)
    
    f = open(filename, 'r')
    
    name = filename.split('.txt')[0]
    f_formatted = open(name + "_formatted.txt", 'w')
    
    # Process each line
    for line in f:
        line = line.replace('\\', "")
        if line.startswith(nslog_start):
            split_line = line.split(nslog_end)
            tweet_text = split_line[1].strip()
            tokens = tweet_text.split(' ')
            for word in tokens:
                word = word.strip()
                if word == "RT" or word.startswith('@') or word.startswith('http') \
                    or word in letter_emoticons:
                    tweet_text = tweet_text.replace(word, '')

            # Tokenize the tweets
            tokens = T.tokenize(tweet_text)
            tweet_text = " ".join(tokens)
            tweet_text = ''.join(c for c in tweet_text if c.isalnum() or c == ' ')
            tweet_text = " ".join(tweet_text.split())
            
            # Strip all words with numbers embedded within
            tok = tweet_text.split()
            for t in tok:
                all_alpha = True
                for c in t:
                    if not c.isalpha():
                        all_alpha = False
                if not all_alpha:
                    tweet_text = tweet_text.replace(t, '')
            tweet_text = " ".join(tweet_text.split())
                   
            # Only write to file if the line isn't empty 
            if tweet_text != '':
                f_formatted.write(tweet_text)
                f_formatted.write('\n')
    f.close()
    f_formatted.close()
    
# Takes files of formatted, stripped tweets and generates
# numbered files containing one tweet each for a given classification
def generate_files(filename, destination_folder):
    f = open(filename, 'r')
    i = 0
    for line in f:
        write_file = open(destination_folder + '/' + \
                          str(i) + '_' + destination_folder + '.txt', 'w')
        write_file.write(line)
        write_file.close()
        i += 1 
    f.close()
    
# This function generates a dictionary containing all of the keywords
# and their counts for a given classifier, and returns the dictionary
def generate_classifier_dictionary(filename):
    f = open(filename, 'r')
    dictionary = {}
    for line in f:
        words = line.split(" ")
        for word in words:
            word = word.strip('\n')
            if len(word) > 2 and word not in stopwords:
                if word in dictionary:
                    dictionary[word] += 1
                else:
                    dictionary[word] = 1
    f.close()
    return dictionary
    
# Takes two dictionaries containing the counts of each token within
# a given classification and then outputs a plist file that is used
# within the iPhone application as the scoring mechanism for each
# tweet
def create_model(pos, neg):
    prob_dict = {}
    # Create probabilities for all positive words that appeared
    for pos_key in pos:
        pos_count = pos[pos_key]
        # Use +1 Smoothing
        if pos_key in neg:
            neg_count = neg[pos_key]
            prob_dict[pos_key] = float(pos_count + 1) / (pos_count + neg_count + 2)
        else:
            prob_dict[pos_key] = float(pos_count + 1) / (pos_count + 2)
    
    # Now check for negative words that weren't in the positive dictionary
    for neg_key in neg:
        if neg_key not in prob_dict:
            neg_count = neg[neg_key]
            prob_dict[neg_key] = 1.0 / (neg_count + 2)
    
    # Now generate the scores
    for key in prob_dict:
        # Subtract .5 from the ration and multiply by 10
        score = ((prob_dict[key] - .5) * 10)
        # Squaring the scores seems to give better results
        # We want to emphasize words that show up very frequently
        # in mostly one category or the other
        if score < 0:
            prob_dict[key] = -(score ** 2)
        else:
            prob_dict[key] = score ** 2
        prob_dict[key] = round(prob_dict[key], 2)
                
    
    print sorted(prob_dict.iteritems(), key=operator.itemgetter(1))
    writePlist(prob_dict, "scores_list.plist")
                
        
# Create the stopword dictionary
stopwords = read_stopwords("stopwords.txt")

# Format the raw tweet data
strip_nslog("positive.txt")
strip_nslog("negative.txt")

# Generate individual files for each tweet
generate_files("positive_formatted.txt", "pos")
generate_files("negative_formatted.txt", "neg")

# Create the dictionary with counts for both positive and negative tweets
pos_dict = generate_classifier_dictionary("positive_formatted.txt")
neg_dict = generate_classifier_dictionary("negative_formatted.txt")

# Build our scoring model and write to file
create_model(pos_dict, neg_dict)


    