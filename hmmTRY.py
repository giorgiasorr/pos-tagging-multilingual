#import numpy as np
from sklearn.metrics import f1_score
from collections import defaultdict, Counter
from itertools import chain
import multiprocessing as mp

def read_data(file_path):
    sentences = []
    sentence = []
    with open(file_path, 'r') as file:
        for line in file:
            if line.strip():
                word, tag = line.strip().split('\t')
                sentence.append((word, tag))
                if word == '.':
                    sentences.append(sentence)
                    sentence = []
    return sentences

train_sentences = read_data('train.col') #Reading English training data
test_sentences = read_data('test.col') #Reading English testing data

# Flattening list of sentences into a list of tagged words
train_tagged_words = list(chain(*train_sentences))

# Creating lists for vocabulary and tags
tokens = [pair[0] for pair in train_tagged_words]
V = set(tokens)
T = set([pair[1] for pair in train_tagged_words])

# Mapping tags to indices
tag_to_index = {tag: index for index, tag in enumerate(T)}
index_to_tag = {index: tag for tag, index in tag_to_index.items()}

# Precomputing emission and transition probabilities
def compute_probabilities(train_tagged_words):
    word_given_tag_dict = defaultdict(Counter)
    tag_given_tag_dict = defaultdict(Counter)
    tag_count = Counter()

    for i, (word, tag) in enumerate(train_tagged_words):
        word_given_tag_dict[tag][word] += 1
        tag_count[tag] += 1
        if i > 0:
            tag_given_tag_dict[train_tagged_words[i-1][1]][tag] += 1

    emission_probs = {tag: {word: (count + 1) / (tag_count[tag] + len(V)) for word, count in words.items()} for tag, words in word_given_tag_dict.items()}
    transition_probs = {t1: {t2: (count + 1) / (tag_count[t1] + len(T)) for t2, count in t2_dict.items()} for t1, t2_dict in tag_given_tag_dict.items()}
    initial_probs = {tag: (count + 1) / (sum(tag_count.values()) + len(T)) for tag, count in tag_count.items()}
    
    return emission_probs, transition_probs, initial_probs

emission_probs, transition_probs, initial_probs = compute_probabilities(train_tagged_words)

# Viterbi algorithm
def Viterbi(words, emission_probs, transition_probs, initial_probs):
    #state = []
    T = list(emission_probs.keys())
    #T_indices = {tag: index for index, tag in enumerate(T)}
    
    # Initializing probabilities
    probs = [{}]
    path = {}
    
    for tag in T:
        probs[0][tag] = initial_probs.get(tag, 1 / len(T)) * emission_probs.get(tag, {}).get(words[0], 1 / len(V))
        path[tag] = [tag]
    
    for i in range(1, len(words)):
        probs.append({})
        new_path = {}
        
        for t in T:
            max_prob, max_state = max((probs[i-1][y0] * transition_probs.get(y0, {}).get(t, 1 / len(T)) * emission_probs.get(t, {}).get(words[i], 1 / len(V)), y0) for y0 in T)
            probs[i][t] = max_prob
            new_path[t] = path[max_state] + [t]
        
        path = new_path
    
    max_prob, max_state = max((probs[len(words) - 1][y], y) for y in T)
    return list(zip(words, path[max_state]))

# Tagging sentences
def tag_sentence(sentence):
    test_words = [tup[0] for tup in sentence]
    return Viterbi(test_words, emission_probs, transition_probs, initial_probs)

def tag_sentences_parallel(test_sentences):
    with mp.Pool(mp.cpu_count()) as pool:
        tagged_sequences = pool.map(tag_sentence, test_sentences)
    return list(chain(*tagged_sequences))

# Testing the model
test_tagged_words = list(chain(*test_sentences))
true_tags = [tup[1] for tup in test_tagged_words]

# Tagging the test sentences
tagged_seq = tag_sentences_parallel(test_sentences)
predicted_tags = [tag for word, tag in tagged_seq]

# Calculating Accuracy, Macro and Micro F1 Scores
accuracy = sum([1 for true, pred in zip(true_tags, predicted_tags) if true == pred]) / len(true_tags)
macro_f1 = f1_score(true_tags, predicted_tags, average='macro')
micro_f1 = f1_score(true_tags, predicted_tags, average='micro')
print(f'Accuracy: {accuracy:.4f}')
print(f'Macro F1 Score: {macro_f1:.4f}')
print(f'Micro F1 Score: {micro_f1:.4f}')

# Writing the output to a file
def write_output(file_path, tagged_sequences):
    with open(file_path, 'w', encoding='utf-8') as file:
        for word, tag in tagged_sequences:
            file.write(f"{word}\t{tag}\n")

write_output('output_en.col', tagged_seq)