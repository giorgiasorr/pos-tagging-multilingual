import numpy as np
from sklearn.metrics import f1_score

def read_data(file_path):
    sentences = []
    sentence = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if line.strip():
                word, tag = line.strip().split('\t')
                sentence.append((word, tag))
                if word == '.' and tag == 'PUNCT':
                    sentences.append(sentence)
                    sentence = []
    if sentence:
        sentences.append(sentence)
    return sentences

# Reading training data
train_sentences = read_data('it_train.col')

# Reading test data
test_sentences = read_data('it_test.col')

# Flattening list of sentences into a list of tagged words
train_tagged_words = [tup for sent in train_sentences for tup in sent]

# List of words 
tokens = [pair[0] for pair in train_tagged_words]

# Vocabulary
V = set(tokens)

# Number of tags
T = set([pair[1] for pair in train_tagged_words])

# Mapping tags to indices
tag_to_index = {tag: index for index, tag in enumerate(T)}
index_to_tag = {index: tag for tag, index in tag_to_index.items()}

# Debugging Information
print(f"Number of sentences in training data: {len(train_sentences)}")
print(f"Number of sentences in test data: {len(test_sentences)}")
print(f"Vocabulary size: {len(V)}")
print(f"Number of tags: {len(T)}")
print(f"Tag to Index Mapping: {tag_to_index}")

# Computing word given tag: Emission Probability
def word_given_tag(word, tag, train_bag=train_tagged_words):
    tag_list = [pair for pair in train_bag if pair[1] == tag]
    count_tag = len(tag_list)
    w_given_tag_list = [pair[0] for pair in tag_list if pair[0] == word]
    count_w_given_tag = len(w_given_tag_list)
    return (count_w_given_tag, count_tag)

# Computing tag given tag: Transition Probability
def t2_given_t1(t2, t1, train_bag=train_tagged_words):
    tags = [pair[1] for pair in train_bag]
    count_t1 = len([t for t in tags if t == t1])
    count_t2_t1 = 0
    for index in range(len(tags) - 1):
        if tags[index] == t1 and tags[index + 1] == t2:
            count_t2_t1 += 1
    return (count_t2_t1, count_t1)

# Transition matrix of tags
tags_matrix = np.zeros((len(T), len(T)))
for i, t1 in enumerate(list(T)):
    for j, t2 in enumerate(list(T)):
        count_t2_t1, count_t1 = t2_given_t1(t2, t1)
        tags_matrix[i, j] = count_t2_t1 / count_t1 if count_t1 > 0 else 0

print("Transition Matrix:")
print(tags_matrix)

# Viterbi algorithm
def Viterbi(words, train_bag=train_tagged_words):
    state = []
    T = list(set([pair[1] for pair in train_bag]))
    T_indices = {tag: index for index, tag in enumerate(T)}
    
    # Initialize probabilities
    probs = [{}]
    path = {}
    
    # Start with initial probabilities
    for tag in T:
        initial_transition_p = 1 / len(T)  # Uniform distribution for initial state
        emission_p = (word_given_tag(words[0], tag)[0] + 1) / (word_given_tag(words[0], tag)[1] + len(V))  # Laplace smoothing
        probs[0][tag] = initial_transition_p * emission_p
        path[tag] = [tag]
    
    print(f"Initial Probabilities: {probs[0]}")
    
    # Forward pass through the sequence
    for i in range(1, len(words)):
        probs.append({})
        new_path = {}
        
        for t in T:
            max_prob, max_state = max((probs[i-1][y0] * tags_matrix[T_indices[y0], T_indices[t]] * 
                                 ((word_given_tag(words[i], t)[0] + 1) / (word_given_tag(words[i], t)[1] + len(V))), y0) for y0 in T)
            probs[i][t] = max_prob
            new_path[t] = path[max_state] + [t]
        
        path = new_path
    
    # Find the final most probable state
    max_prob, max_state = max((probs[len(words) - 1][y], y) for y in T)
    return list(zip(words, path[max_state]))

# Function to tag sentences
def tag_sentences(test_sentences):
    tagged_sequences = []
    for sentence in test_sentences:
        test_words = [tup[0] for tup in sentence]
        tagged_seq = Viterbi(test_words)
        tagged_sequences.extend(tagged_seq)
    return tagged_sequences

# Function to write the output to a .col file
def write_output(file_path, tagged_sequences):
    with open(file_path, 'w', encoding='utf-8') as file:
        for word, tag in tagged_sequences:
            file.write(f"{word}\t{tag}\n")

# Testing the model
test_tagged_words = [tup for sent in test_sentences for tup in sent]
true_tags = [tup[1] for tup in test_tagged_words]

# Tagging the test sentences
tagged_seq = tag_sentences(test_sentences)
predicted_tags = [tag for word, tag in tagged_seq]

# Calculate accuracy
accuracy = sum([1 for true, pred in zip(true_tags, predicted_tags) if true == pred]) / len(true_tags)
print(f'Accuracy: {accuracy:.4f}')

# Calculate Macro and Micro F1 Scores
macro_f1 = f1_score(true_tags, predicted_tags, average='macro')
micro_f1 = f1_score(true_tags, predicted_tags, average='micro')
print(f'Macro F1 Score: {macro_f1:.4f}')
print(f'Micro F1 Score: {micro_f1:.4f}')

# Write the output to a file
write_output('output_it.col', tagged_seq)