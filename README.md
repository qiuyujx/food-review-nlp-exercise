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
`Wow... Loved this place.` -> `Wow Loved this place`

2. Remove stop words
`Wow Loved this place` -> `Wow Loved place`

3. POS (part of speech) labelling & filtering


4. Words lemmatization

5. Bag of words & review vectors generating

6. Training (Naive Bayes)

7. Training (More to be added)
TODO


# Future Works

- Classify a file with multiple food reviews
- Unit testing
- More different algorithms other than Naive Bayes