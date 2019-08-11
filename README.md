
# food-review-nlp-exercise

This is an exercise for sentiment analysis based on python-nltk.

# Installation

```
$ python setup.py install
```

# Features

## Train a model from a TSV file

This will train a model with default name "default_model".

```
$ foodrw -t "data\train.txt"
```

Note: If default_model exists, this will overwrite it.

Train a model with customized model name. The code below will train a model named "my_model"

```
$ foodrw -t "data\train.txt" -m "my_model"
```

## Classify a review text

Classify a review text. It come with its probability (relavence scores) of being Positive/Negtive

```
$ foodrw -q "An extensive menu provides lots of options for breakfast."

Output:
This review is classified as **Positive**, with probability 0.971040.
```

## Classify multiple reviews in a file

Classify a file with multiple reviews. The file must contain one reviews each new line.

```
$ foodrw -f "data\test.txt"
```

Optionally, you can specify the name of the model want to use, as well as customize the path of the classified file name.

```
$ foodrw -f "data\test.txt" -m test_model -d "data\my_classified.txt"
```

# Methodology

1. Remove punctuation

E.g.

`Wow... Loved this place.` -> `Wow Loved this place`

1. Tokenisation

Separate words and put them into an array/list

E.g.

`Wow Loved this place` -> `['Wow', 'Loved', 'this', 'place']`

1. Remove stop words

Stop words are those used very commonly and meaningless, such as "the", "a", "this" and "that".

E.g.

`['Wow', 'Loved', 'this', 'place']` -> `['Wow', 'Loved', 'place']`

1. POS (part of speech) labelling & filtering

POS indicates the category to which a word is assigned in accordance with its syntactic functions

E.g.

`['Wow', 'Loved', 'place']` -> `[('Wow', 'NNP'), ('Loved', 'VBD'), ('place', 'NN')]`

5. Words lemmatization

Recover word into its original form, such as plural to single or past tense to present tense

E.g.

`[('Wow', 'NNP'), ('Loved', 'VBD'), ('place', 'NN')]` -> `[('wow', 'NNP'), ('love', 'VBD'), ('place', 'NN')]`

6. Bag of words & review vectors generating

All the words from all reviews are collected into a list with their occurrence frequencies. These words are filtered based on their frequencies. That is, words are reserved only if they occurred frequently. Finally, a feature (every words) vector is generated.

For every single review, we'll look at words it contains. If any words in the feature list occur, the corresponding boolean value of the word is set to True, otherwise remain to be False.

Therefore, each review is converted into a feature vector. For example, the review `Wow... Loved this place.` is converted into the vector as follows:

```
{
    'wow': True,
    'love': True,
    'place': True,
    'stopped': False,
    'late': False,
    'recommendation': False,
    'selection': False,
    ...
    'undercooked': False
}
```

1. Training (Naive Bayes)

Naive Bayes Classifier Algorithm is a family of probabilistic algorithms based on applying Bayes’ theorem with the “naive” assumption of conditional independence between every pair of a feature.

We classify whether the review `Wow... Loved this place.` is a positive review or a negative review. 

We then have to calculate:

P(positive | wow love place) — the probability that the tag of a sentence is positive given that the sentence is `Wow... Loved this place.`.

P(negative | wow love place) — the probability that the tag of a sentence is negative given that the sentence is `Wow... Loved this place.`.

**_TODO: More algorithms such as logistic regression can be added._**

1. Relevance score

Because we are using Naive Bayes, the probability of the classification can be simply used as its "relevance score".

For example:

```
This review is classified as **Positive**, with probability 0.983745.
```

In the above output, the probability `0.983745` means this review has 98.37% probability to be a positive review.

# Assumptions and trade-off

Currently we are extracting words with POS noun, verb, adjective and adverb. This is because the training set is tend to be small. To avoid too many "empty" vectors, which means that no word can be found in the feature list, I involved all of these POS. However, when we have a relatively larger training set, we may only need to consider adjectives and adverbs which potentially make more sense in expressing positive/negative sentiments.


# Future Works

- Unit testing
- More algorithms other than Naive Bayes, such as Multinomial Naive Bayes, Bernoulli Naive Bayes, Logistic Regression, Stochastic Gradient Descent and Support Vector Classifier.
