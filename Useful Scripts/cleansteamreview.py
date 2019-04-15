#cleans up the steam review from the scraper

import numpy as np
import pandas as pd
import ast
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from sklearn.decomposition import NMF, LatentDirichletAllocation, TruncatedSVD
from sklearn.feature_extraction.text import CountVectorizer

data = []

with open('witcherfakejson.txt', encoding="utf-8") as f:  
    for line in f:
        data.append(line)

stripped_data = [review.replace('\n', "").replace('\\n', "").replace('true', 'True').replace('false', 'False') for review in data]

eval_data = [ast.literal_eval(review) for review in stripped_data]

#texts = [(review['text'] + '\n') for review in eval_data]
texts = [review['text'] for review in eval_data]

#remove game name
#texts = [review.replace('slay', "").replace('spire', "") for review in texts]
#texts = [review.replace('Slay', "").replace('Spire', "") for review in texts]   

#write texts to text file
with open('outputwitcher.txt', "w") as f:
	f.writelines(texts)

for review in eval_data[0:1000]:
    texts.append(review['text'])
