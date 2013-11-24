Twitter-Sentiment-Analyzer-Model-Builder
========================================

Code used to manipulate fetched tweets and build the scoring model used for the iPhone Twitter Sentiment Analyzer

NOTE: This code was written in conjunction with an iPhone application used to do realtime tweet sentiment analysis based on keyword input. The code for that project can also be found in my public repositories underneath Twitter-Sentiment-Analyzer.

Components
----------

negative.txt
  - Approximately 7,000 unprocessed tweets with negative sentiment emoticons

positive.txt
  - Approximately 7,000 unprocessed tweets with positive sentiment emoticons
  
negative_formatted.txt
  - Processed tweets from negative.txt using modelBuilder.py
  
positive_formatted.txt
  - Processed tweets from positive.txt using modelBuilder.py
  
stopwords.txt
  - a list of stopwords delineated by commas used in modelBuilder.py to factor out words that would hinder our naive bayes sentiment analysis
  
twitter_tokenizer.py
  - a tokenizer written especially for Twitter by Christopher Potts
  
pos
  - A directory containing each of the tweets from positive_formatted.txt arranged into files of one tweet per file
  
neg
  - A directory containing each of the tweets from negative_formatted.txt arranged into files of one tweet per file
  
scores_list.plist
  - The file created by modelBuilder.py containing the scores of each stopword-excluded keyword. The scoring was based on naive bayes classification.
  
modelBuilder.py
  - The main file used for processing the raw tweets and transforming the information into a property list that can be used later for the Twitter Sentiment Analyzer iPhone application that I wrote. The code for that project can be found in my public repositories under Twitter-Sentiment-Analyzer.
