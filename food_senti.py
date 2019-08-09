import os
import re
import random
import math
import nltk
import pickle
from datetime import datetime as dt
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

'''
    Helper functions
'''
# Timestamp
def time():
    return '[' + dt.now().strftime("%Y-%m-%d %H:%M:%S.%f") + '] '

# Download nltk resource packages
print(time()+'Check nltk packages, download if not')
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

'''
    Constants
'''
# Select word types
'''
    J -> adjective
    R -> adverb
    V -> verb
    N -> noun
'''
w_types = ['J', 'V', 'R', 'N']

# Load stop words
stop_words = list(set(stopwords.words('english')))

# Init Lemmatizer
lemmatizer = WordNetLemmatizer()

# Targets
tg_dict = {
    0: 'Negative',
    1: 'Positive'
}


'''
    Utility functions
'''

def get_md_files(model_name):
    return '.\\model\\'+model_name+'.classifier', '.\\model\\'+model_name+'.words'

def parse_review(r):
        bow = []
        # remove punctuations
        cleaned = re.sub(r'[^(a-zA-Z)\s]','', r)
        # Tokenise
        tokenized = word_tokenize(cleaned)
        # Remove stop words
        stopped = [w for w in tokenized if not w in stop_words]
        # Part of Speed labelling 
        labelled = nltk.pos_tag(stopped)
        # Reserve word types needed
        for w in labelled:
            w_type = w[1][0]
            if w_type in w_types:
                word = w[0].lower()
                if w_type == 'V': # convert verbs to present tense
                    word = lemmatizer.lemmatize(word, 'v')
                if w_type == 'N': # convert noun to single form
                    word = lemmatizer.lemmatize(word)
                bow.append(word)
        return bow

def rw_to_vec(r, all_words):
        bow = parse_review(r)
        vec = {}
        for w in all_words:
            vec[w] = (w in bow)
        return vec


'''
    Train a model from a given file
    Save the trained model to a binary file
'''
def train_model(tr_file, model_name):

    # Read reviews from training file
    print(time()+'Reading file: ' + tr_file)
    reviews = open(tr_file, 'r').read().split('\n')
    reviews = [line.split('\t') for line in reviews]
    print(time()+'Totally %d reviews loaded' % len(reviews))

    # Validate reviews strings
    for r in reviews:
        if len(r) is not 2:
            print(time()+'Rejected invalid line: ', str(r))
            reviews.remove(r)

    # Split positive and negative reviews
    rw_pos = [r[0] for r in reviews if r[1] == '1']
    rw_neg = [r[0] for r in reviews if r[1] == '0']
        
    # Extract all selected words from parsed reviews
    print(time()+'Extracting informative words')
    all_words = []
    for r in rw_pos+rw_neg:
        all_words = all_words + parse_review(r)
    
    # Get words frequency
    all_words = nltk.FreqDist(all_words)

    # Reject low frequency words
    all_words = [word for word, freq in all_words.items() if freq > 1]

    # parse reviews to vectors    
    print(time()+'Parsing reivews')
    rw_pos_vecs = [(rw_to_vec(r, all_words), 1) for r in rw_pos]
    rw_neg_vecs = [(rw_to_vec(r, all_words), 0) for r in rw_neg]

    # Filter review vectors that has no word matched, combine all vectors to 1 list
    rw_vecs = []
    for tp in rw_pos_vecs + rw_neg_vecs:
        vec = tp[0]
        wd_matched = [k for k,v in vec.items() if v]
        if len(wd_matched) > 0:
            rw_vecs.append(tp)
    
    # Shuffle the vectors
    random.shuffle(rw_vecs)

    # Split train & test set
    print(time()+'Training model')
    train_set_pct = 0.8
    split_num = math.floor(len(rw_vecs) * train_set_pct)
    train_set = rw_vecs[:split_num]
    test_set = rw_vecs[split_num:]

    # Train the model (classifier)
    model = nltk.NaiveBayesClassifier.train(train_set)    

    # Show accuracy and most informative features
    print("Classifier accuracy percent:",(nltk.classify.accuracy(model, test_set))*100)
    model.show_most_informative_features(20)

    # Serialise model and save as file
    print(time()+'Serialising model to binary file')
    m_file, w_file = get_md_files(model_name)
    with open(m_file, 'wb') as md_writer:
        pickle.dump(model, md_writer)

    # Save feature words to file
    with open(w_file, 'w') as wd_writer:
        for w in all_words:
            wd_writer.write('%s\n' % w)
    
    print(time()+'All done. You can use "python main.py -m %s -q <review>" option to classify reviews now.' % model_name)


def make_prediction(q_text, model_name):
    # Load model
    m_file, w_file = get_md_files(model_name)
    all_words = []
    with open(w_file, 'r') as wd_reader:
        for line in wd_reader:
            line = line[:-1]
            all_words.append(line)
    with open(m_file, 'rb') as md_reader:
        model = pickle.load(md_reader)
    
    # Classify
    prob_dist = model.prob_classify(rw_to_vec(q_text, all_words))
    target = prob_dist.max()
    probability = prob_dist.prob(target)
    
    # Show result
    print('This review is classified as %s, with probability %f.' % tg_dict[target], probability)
    