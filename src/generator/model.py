import numpy as np

text = open('qoutes.txt').read()

corpus = text.split()


def make_pairs(corpus):
    for i in range(len(corpus) - 1):
        yield (corpus[i], corpus[i + 1])


pairs = make_pairs(corpus)

words_dict = {}

for word_1, word_2 in pairs:
    if word_1 in words_dict.keys():
        words_dict[word_1].append(word_2)
    else:
        words_dict[word_1] = [word_2]

first_word = np.random.choice(corpus)

# делаем так, чтобы первое слово начиналось с большой буквы
while first_word.islower():
    first_word = np.random.choice(corpus)

chain = [first_word]

n_words = 100

for i in range(n_words):
    chain.append(np.random.choice(words_dict[chain[-1]]))

print(' '.join(chain))
