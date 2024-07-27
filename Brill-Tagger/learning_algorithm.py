from collections import defaultdict, Counter
import copy
import operator
import sys
import os
import evaluation
import collections
from collections import defaultdict


train_file = os.path.join(sys.path[0], "test.col")
gold_standard_file = os.path.join(sys.path[0], "test.col")
L_train_file = os.path.join(sys.path[0], "train.col")


#### Create a corpus without tags ####


def create_corpus_C(training_file):
    "reads the test.col line by line and creates a corpus with only words from test.col each empty line represents the end of a sentence."
    sentences = []
    current_sentence = []

    with open(training_file, "r") as file:
        with open(os.path.join(sys.path[0], "corpus_without_tags_english.txt"), "w") as fp:
            for line in file:
                if line.strip():
                    word, tag = line.split()
                    current_sentence.append((word))
                    fp.write("%s\n" % word)
                else:
                    if current_sentence:
                        sentences.append(current_sentence)
                        fp.write("%s\n" % "")
                        current_sentence = []
    if current_sentence:
        sentences.append(current_sentence)

    return sentences


create_corpus_C(train_file)

#### Create a corpus without tags ####


#### parse corpus sentence wise ####


def parse_training_data(training_file):
    "Read corpus, the variable sentence has all the sentences [[..],[..],[..]...]"
    sentences = []
    current_sentence = []

    with open(training_file, "r") as file:
        for line in file:
            if line.strip():  # Non-empty line
                word, tag = line.split()
                current_sentence.append((word, tag))
            else:  # Empty line indicates end of sentence
                if current_sentence:
                    sentences.append(current_sentence)
                    current_sentence = []

    # Append the last sentence if it's not empty and doesn't end with an empty line
    if current_sentence:
        sentences.append(current_sentence)

    return sentences


#### parse corpus sentence wise ####


#### convert corpus sentence to a word : tag Dictionary ####
# the : DT 7, NN 2
def build_word_to_tag_dict(sentences):
    "Read data from parse_training_data and convert it to a dict, [ example : 'The': {'DT': 205, 'NNP': 2}...]"
    "Only using this for testing wether the model can perform pos tagging for a sentence"
    word_to_tag = {}

    for sentence in sentences:
        for word, tag in sentence:
            if word not in word_to_tag:
                word_to_tag[word] = {}
            if tag in word_to_tag[word]:
                word_to_tag[word][tag] += 1
            else:
                word_to_tag[word][tag] = 1

    return word_to_tag


#### convert corpus sentence to a word : tag Dictionary ####


#### calculate possible tags for each word ####
def calculate_possible_tags(word_to_tag):
    "Read train.col for this because it has a lot of data, write it in a descending order to a file possible_tags_english.txt [ example : {'in': {'IN': 560, 'RP': 8, 'RB': 2}}"
    word_to_majority_tag = {}
    all_posible_tags = {}
    for word, tag_counts in word_to_tag.items():
        all_posible_tags[word] = tag_counts
        majority_tag = max(tag_counts, key=tag_counts.get)
        word_to_majority_tag[word] = majority_tag
    new_dict = {}
    with open(os.path.join(sys.path[0], "possible_tags_english.txt"), "w") as fp:
        for i in all_posible_tags:
            sorted_d = dict(
                sorted(
                    all_posible_tags[i].items(),
                    key=operator.itemgetter(1),
                    reverse=True,
                )
            )
            new_dict[i] = sorted_d
            fp.write("%s\n" % {i: sorted_d})
    return new_dict



#### calculate possible tags for each word ####


predicted_parsed = parse_training_data(L_train_file)
gold_standard_parsed = parse_training_data(gold_standard_file)
word_to_tag = build_word_to_tag_dict(predicted_parsed)
word_to_possible_tags = calculate_possible_tags(word_to_tag)


All_possible_tags = os.path.join(sys.path[0], "possible_tags_english.txt")
Corpus_without_tags = os.path.join(sys.path[0], "corpus_without_tags_english.txt")




#### annotate the corpus with majority tag ####




def read_and_map_files(file1_path, file2_path, output_path):
    "read both possible_tags.txt and corpus_without_tags_english.txt. Annotate the corpus_without_tags_english with the most frequent tag for each word from possible_tags. Assign UNK (unknown) tag for unknown words"
    word_to_tag = {}  # Dictionary to store mappings from file 1

    # Read and parse file 1
    with open(file1_path, "r") as file1:
        for line in file1:
            entry = eval(line.strip())
            word = list(entry.keys())[0]  # take only the words
            tag_dict = entry[word]  # take all the values
            first_tag = list(tag_dict.keys())[0]  # take only the 1st value
            word_to_tag[word] = first_tag  # the : DT

    # Read file 2 and perform mapping
    mapped_words = []
    with open(file2_path, "r") as file2:
        for line in file2:
            word = line.strip()
            if word in word_to_tag:
                mapped_words.append(
                    (word, word_to_tag[word])
                )  # Map the word to its corresponding tag from file 1
            elif word == "":
                mapped_words.append(("", ""))
            else:
                mapped_words.append(
                    (word, "UNK")
                )  # use 'UNK' (unknown) as a placeholder If the word is not found in file

    with open(output_path, "w") as output_file:
        for word, tag in mapped_words:
            output_file.write(f"{word}   {tag}\n")

    return mapped_words


Annotated_corpus_majority_tags = os.path.join(sys.path[0], "annotated_corpus_english.txt")
mapped_words = read_and_map_files(
    All_possible_tags, Corpus_without_tags, Annotated_corpus_majority_tags
)




#### annotate the corpus with majority tag ####


Annotated_parsed = parse_training_data(Annotated_corpus_majority_tags)



#### evaluate ####




all_tags = []
with open(Annotated_corpus_majority_tags, "r") as file:
    for line in file:
        if line.strip():
            word, tag = line.split()
            all_tags.append(tag)
counter = collections.Counter(all_tags)
labels =[]
for i in set(all_tags):
    labels.append(i)

# evaluate(gold_standard_parsed, final_parsed, labels)




#### evaluate ####





##### clean data again #####

gold_matrix = []
with open(gold_standard_file, "r") as file:
    for line in file:
        if line.strip():  # Non-empty line
            word, tag = line.split()
            gold_matrix.append((word, tag))
        else:  # Empty line indicates end of sentence
            next

final_matrix = []
with open(Annotated_corpus_majority_tags, "r") as file:
    for line in file:
        if line.strip():  # Non-empty line
            word, tag = line.split()
            final_matrix.append((word, tag))
        else:  # Empty line indicates end of sentence
            next


##### clean data again #####




def generate_confusion_table(transformed_corpus, gold_standard):
    confusion_table = defaultdict(int)
    for (transformed_word, transformed_tag), (gold_word, gold_tag) in zip(transformed_corpus, gold_standard):
        if transformed_tag != gold_tag:
            confusion_table[(transformed_tag, gold_tag)] += 1
    return confusion_table


confusion_table1 = generate_confusion_table(final_matrix, gold_matrix)




     

def analyze_and_apply_transformations(gold_data, initial_data, confusion_matrix):
    def get_context(tagged_sentence, index):
        """ Get the previous and next tag for a given index in a tagged sentence """
        prev_tag = tagged_sentence[index-1][1] if index > 0 else None
        next_tag = tagged_sentence[index+1][1] if index < len(tagged_sentence)-1 else None
        return prev_tag, next_tag

    context_patterns = defaultdict(list)
    for i_sentence, sentence in enumerate(gold_data):
        for i_word, (word, correct_tag) in enumerate(sentence):
            prev_tag, next_tag = get_context(sentence, i_word)
            context_patterns[correct_tag].append((prev_tag, next_tag))
    final_rules = []
    for (incorrect_tag, correct_tag), _ in confusion_matrix.items():
        pattern_counts = Counter(context_patterns[correct_tag])
        best_pattern = None
        best_error_count = float('inf')

        for pattern in pattern_counts:
            test_data = copy.deepcopy(initial_data)
            for i_sentence, sentence in enumerate(test_data):
                for i_word, (word, tag) in enumerate(sentence):
                    if tag == incorrect_tag:
                        prev_tag, next_tag = get_context(sentence, i_word)
                        if (prev_tag, next_tag) == pattern:
                            test_data[i_sentence][i_word] = (word, correct_tag)
            new_confusion_matrix = calculate_confusion_matrix(gold_data, test_data)
            error_count = sum(new_confusion_matrix.values())

            if error_count < best_error_count:
                best_error_count = error_count
                best_pattern = pattern

        if best_pattern:
            final_rules.append((incorrect_tag, correct_tag, best_pattern))
    final_data = copy.deepcopy(initial_data) 
    for incorrect_tag, correct_tag, pattern in final_rules:
        for i_sentence, sentence in enumerate(final_data):
            for i_word, (word, tag) in enumerate(sentence):
                if tag == incorrect_tag:
                    prev_tag, next_tag = get_context(sentence, i_word)
                    if (prev_tag, next_tag) == pattern:
                        final_data[i_sentence][i_word] = (word, correct_tag)

    return final_data, final_rules

def calculate_confusion_matrix(gold_data, test_data):
    confusion_matrix = defaultdict(int)
    for gold_sentence, test_sentence in zip(gold_data, test_data):
        for (gold_word, gold_tag), (test_word, test_tag) in zip(gold_sentence, test_sentence):
            if gold_tag != test_tag:
                confusion_matrix[(test_tag, gold_tag)] += 1
    return confusion_matrix

final_data, final_rules = analyze_and_apply_transformations(gold_standard_parsed, Annotated_parsed, confusion_table1)

# print("Final Data:", final_data)
# print("Final Rules Applied:", final_rules)

def write_final_data_to_file(final_data, output_file):
    with open(output_file, "w") as file:
        for sentence in final_data:
            for word, tag in sentence:
                file.write(f"{word}\t{tag}\n")
            file.write("\n")  

output_file_path = os.path.join(sys.path[0], "final_data.txt")
write_final_data_to_file(final_data, output_file_path)

print(f"Final data written to {output_file_path}")

learning_output = parse_training_data(output_file_path)
learning_algorithm_evaluation = evaluation.evaluate(gold_standard_parsed, learning_output, labels)
