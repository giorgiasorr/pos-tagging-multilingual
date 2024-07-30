from sklearn.metrics import f1_score
from collections import defaultdict, Counter
from itertools import chain
import multiprocessing as mp


def read_data(file_path):
    """
    Reads data from given file path and returns a list of sentences,
    where each sentence is a list of (word, tag) tuples.
    """
    sentences = []
    sentence = []
    with open(file_path, "r") as file:
        for line in file:
            if line.strip():  # Checks if the line is not empty
                word, tag = line.strip().split("\t")
                sentence.append((word, tag))
                if word == ".":  # End of a sentence
                    sentences.append(sentence)
                    sentence = []
    return sentences


# Reading English training and testing data
train_sentences = read_data("en_train.col")
test_sentences = read_data("en_test.col")

# Flattening list of sentences into a list of tagged words
train_tagged_words = list(chain(*train_sentences))

# Creating lists for vocabulary and tags
tokens = [pair[0] for pair in train_tagged_words]  # Extracting words
V = set(tokens)  # Vocabulary (Set of unique tokens)
T = set([pair[1] for pair in train_tagged_words])  # Set of unique tags

# Mapping tags to indices
tag_to_index = {tag: index for index, tag in enumerate(T)}
index_to_tag = {index: tag for tag, index in tag_to_index.items()}


def compute_probabilities(train_tagged_words):
    """
    Computes emission and transition probabilities from training data.
    Returns dictionaries for emission_probs, transition_probs, and initial_probs.
    """
    word_given_tag_dict = defaultdict(Counter)
    tag_given_tag_dict = defaultdict(Counter)
    tag_count = Counter()

    for i, (word, tag) in enumerate(train_tagged_words):
        word_given_tag_dict[tag][word] += 1
        tag_count[tag] += 1
        if i > 0:
            # Incrementing transition count for the previous tag to the current tag
            tag_given_tag_dict[train_tagged_words[i - 1][1]][tag] += 1

    # Emission probabilities with Laplace smoothing
    emission_probs = {
        tag: {
            word: (count + 1) / (tag_count[tag] + len(V))
            for word, count in words.items()
        }
        for tag, words in word_given_tag_dict.items()
    }
    # Transition probabilities with Laplace smoothing
    transition_probs = {
        t1: {
            t2: (count + 1) / (tag_count[t1] + len(T)) for t2, count in t2_dict.items()
        }
        for t1, t2_dict in tag_given_tag_dict.items()
    }
    # Initial probabilities with Laplace smoothing
    initial_probs = {
        tag: (count + 1) / (sum(tag_count.values()) + len(T))
        for tag, count in tag_count.items()
    }

    return emission_probs, transition_probs, initial_probs


# Precomputing emission and transition probabilities
emission_probs, transition_probs, initial_probs = compute_probabilities(
    train_tagged_words
)


def Viterbi(words, emission_probs, transition_probs, initial_probs):
    """
    Implements the Viterbi algorithm.
    Returns the most probable sequence of tags for the given words.
    """
    T = list(emission_probs.keys())  # List of unique tags

    # Initializing probabilities and path dictionaries
    probs = [{}]
    path = {}

    # First: calculating probabilities for the first word
    for tag in T:
        probs[0][tag] = initial_probs.get(tag, 1 / len(T)) * emission_probs.get(
            tag, {}
        ).get(words[0], 1 / len(V))
        path[tag] = [tag]

    # Then: calculating probabilities for the rest of the words
    for i in range(1, len(words)):
        probs.append({})
        new_path = {}

        for t in T:
            # Finding the maximum probability for the current tag t
            max_prob, max_state = max(
                (
                    probs[i - 1][y0]
                    * transition_probs.get(y0, {}).get(t, 1 / len(T))
                    * emission_probs.get(t, {}).get(words[i], 1 / len(V)),
                    y0,
                )
                for y0 in T
            )
            probs[i][t] = max_prob
            new_path[t] = path[max_state] + [t]

        path = new_path

    # Finding the final most probable state
    max_prob, max_state = max((probs[len(words) - 1][y], y) for y in T)
    return list(zip(words, path[max_state]))


def tag_sentence(sentence):
    """
    Tags a single sentence using the Viterbi algorithm.
    Returns a list of (word, tag) tuples.
    """
    test_words = [tup[0] for tup in sentence]
    return Viterbi(test_words, emission_probs, transition_probs, initial_probs)


def tag_sentences_parallel(test_sentences):
    """
    Tags all sentences in the test set using parallel processing.
    Returns a flattened list of tagged words.
    """
    with mp.Pool(mp.cpu_count()) as pool:
        tagged_sequences = pool.map(tag_sentence, test_sentences)
    return list(chain(*tagged_sequences))


# Flattening test sentences to get true tags
test_tagged_words = list(chain(*test_sentences))
true_tags = [tup[1] for tup in test_tagged_words]

# Tagging the test sentences
tagged_seq = tag_sentences_parallel(test_sentences)
predicted_tags = [tag for _, tag in tagged_seq]

# Calculating Accuracy, Macro and Micro F1 Scores
accuracy = sum(
    [1 for true, pred in zip(true_tags, predicted_tags) if true == pred]
) / len(true_tags)
macro_f1 = f1_score(true_tags, predicted_tags, average="macro")
micro_f1 = f1_score(true_tags, predicted_tags, average="micro")
print(f"Accuracy: {accuracy:.4f}")
print(f"Macro F1 Score: {macro_f1:.4f}")
print(f"Micro F1 Score: {micro_f1:.4f}")


""" Writing the output to a file
def write_output(file_path, tagged_sequences):
    with open(file_path, 'w', encoding='utf-8') as file:
        for word, tag in tagged_sequences:
            file.write(f"{word}\t{tag}\n")

write_output('output_hmm_en.col', tagged_seq)
"""
