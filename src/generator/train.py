import codecs
import argparse
import re
import numpy as np

def generate_ngrams(text, n=2):
    pattern = re.compile('[\W_]+')
    clean_text = pattern.sub(' ', text)
    clean_text = clean_text.lower()
    words = clean_text.split()

    dictionary = dict.fromkeys(words, [])
    for i in range(0, len(words) - 1):
        dictionary[words[i]] = dictionary[words[i]] + words[i + 1].split()

    dictionary[words[len(words) - 1]] = dictionary[words[len(words) - 1]] + words[0].split()
    return dictionary


def generate(var, count):
    text = codecs.open("variations/"+str(var)+".txt", 'r', 'utf-8').read()

    ngrams = generate_ngrams(text)
    next_word = np.random.choice(ngrams, 1)[0]
    result = ''
    for i in range(0, count):
        result += next_word + " "
        next_word = 1


