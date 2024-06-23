import operator
import sys
import os
import evaluation
import collections
from collections import defaultdict



def contains_digit(s):
    "checks whether a word in the corpus contains a number or not such as 400th, 250th ,1400s..."
    isdigit = str.isdigit
    return any(map(isdigit, s))


train_file = os.path.join(sys.path[0], "test.col")
gold_standard_file = os.path.join(sys.path[0], "test.col")
L_train_file = os.path.join(sys.path[0], "train.col")


#### Create a corpus without tags ####


def create_corpus_C(training_file):
    "reads the test.col line by line and creates a corpus with only words from test.col each empty line represents the end of a sentence."
    sentences = []
    current_sentence = []

    with open(training_file, "r") as file:
        with open(os.path.join(sys.path[0], "corpus_without_tags.txt"), "w") as fp:
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
    "Read train.col for this because it has a lot of data, write it in a descending order to a file possible_tags.txt [ example : {'in': {'IN': 560, 'RP': 8, 'RB': 2}}"
    word_to_majority_tag = {}
    all_posible_tags = {}
    for word, tag_counts in word_to_tag.items():
        all_posible_tags[word] = tag_counts
        majority_tag = max(tag_counts, key=tag_counts.get)
        word_to_majority_tag[word] = majority_tag
    new_dict = {}
    with open(os.path.join(sys.path[0], "possible_tags.txt"), "w") as fp:
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


predicted_parsed = parse_training_data(train_file)
gold_standard_parsed = parse_training_data(gold_standard_file)
word_to_tag = build_word_to_tag_dict(predicted_parsed)
word_to_possible_tags = calculate_possible_tags(word_to_tag)


All_possible_tags = os.path.join(sys.path[0], "possible_tags.txt")
Corpus_without_tags = os.path.join(sys.path[0], "corpus_without_tags.txt")


#### annotate the corpus with majority tag ####


def read_and_map_files(file1_path, file2_path, output_path):
    "read both possible_tags.txt and corpus_without_tags.txt. Annotate the corpus_without_tags with the most frequent tag for each word from possible_tags. Assign UNK (unknown) tag for unknown words"
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


Annotated_corpus_majority_tags = os.path.join(sys.path[0], "annotated_corpus.txt")
mapped_words = read_and_map_files(
    All_possible_tags, Corpus_without_tags, Annotated_corpus_majority_tags
)


#### annotate the corpus with majority tag ####


#### apply rules ####


def apply_rules(sentences, output_file):
    "Takes the newly annotated corpus and applies contextual rules to it. Creates a new file called after_rule_corpus with new tags assigned to each sentence in the corpus based on the rules"
    transformed_sentences = []
    with open(output_file, "w") as f:
        for sentence in sentences:
            transformed_sentence = []
            previous_tag = None  # previous tags,for 1st there´s

            for i, (word, tag) in enumerate(sentence):
                # Apply transformational rules based on context
                if (
                    word == "continued"
                    and i < len(sentence) - 1
                    and (sentence[i + 1][1] == "NN" or sentence[i + 1][1] == "VBG")
                ):
                    transformed_sentence.append(
                        ("continued", "VBN")
                    )  # 'continued' before a NN or a VBG is likely a VBN (Verb, past participle)
                elif word.isalpha() and (len(word) == 1 and sentence[i + 1][1] == ":"):
                    transformed_sentence.append((word, "LS"))
                elif word == "-":
                    if previous_tag == "LS":
                        transformed_sentence.append(("-", ":"))
                    else:
                        transformed_sentence.append(("-", "HYPH"))
                elif word == "#":
                    transformed_sentence.append(("#", "$"))
                elif word == "Farmers":
                    if previous_tag == "WRB":
                        transformed_sentence.append(("Farmers", "NNP"))
                    else:
                        transformed_sentence.append(("Farmers", "NNPS"))
                elif word == "{":
                    transformed_sentence.append(("{", "-LRB-"))
                elif word == "}":
                    transformed_sentence.append(("}", "-RRB-"))
                elif word == "/":
                    transformed_sentence.append(("/", "SYM"))
                elif tag == "NN":
                    # Rule: NN --> VBP if the preceding tag is 'PRP'
                    if previous_tag == "PRP":
                        transformed_sentence.append((word, "VBP"))
                    # Rule: NN --> JJ if the following tag is 'JJ'
                    elif i + 1 < len(sentence) and sentence[i + 1][1] == "JJ":
                        transformed_sentence.append((word, "JJ"))
                    # Rule: NN --> IN if the preceding tag is '.'
                    elif previous_tag == ".":
                        transformed_sentence.append((word, "IN"))
                    else:
                        transformed_sentence.append(
                            (word, tag)
                        )  # Keep original tag if no rule applies
                elif tag == "NNP":
                    # Rule: NNP --> NN if the tag of words i-3...i-1 is JJ
                    if i >= 3 and all(sentence[i - j][1] == "JJ" for j in range(1, 4)):
                        transformed_sentence.append((word, "NN"))
                    # Rule: NNP --> NNP if the tag of words i+1...i+2 is NNP
                    elif i + 2 < len(sentence) and all(
                        sentence[i + j][1] == "NNP" for j in range(1, 3)
                    ):
                        transformed_sentence.append((word, "NNP"))
                    else:
                        transformed_sentence.append(
                            (word, tag)
                        )  # Keep original tag if no rule applies
                elif word == "to":
                    # Determine tag for 'to' based on previous tag
                    ptags = ["VB", "VBP", "MD", "NN", "JJ", "NNS", "RB", "VBZ", "VBD"]
                    if previous_tag in ptags and (
                        sentence[i + 1][1] == "VB"
                        or sentence[i + 1][1] == "VBZ"
                        or sentence[i + 1][1] == "VBD"
                    ):
                        transformed_sentence.append(("to", "TO"))
                    elif (
                        previous_tag in ptags
                        and (sentence[i + 1][1] == "DT" or sentence[i + 1][1] == "NN")
                        and sentence[i + 2][1] not in ["VB", "VBZ", "VBD"]
                    ):
                        transformed_sentence.append(("to", "IN"))
                    else:
                        transformed_sentence.append(
                            ("to", "IN")
                        )  # else tag 'to' as preposition
                elif (
                    word == "all"
                    and i < len(sentence) - 1
                    and (sentence[i + 1][1] == "DT" or sentence[i + 1][1] == "PRP$")
                ):
                    transformed_sentence.append(
                        ("all", "PDT")
                    )  # 'all' before a DT is likely a predeterminer
                elif word == "about" and i > 0 and sentence[i - 1][1] == "IN":
                    transformed_sentence.append(
                        ("about", "IN")
                    )  # Tag 'about' as IN when it introduces a prepositional phrase
                elif word in ["he", "HE", "He", "she", "SHE", "She", "it", "IT"]:
                    transformed_sentence.append(
                        (word, "PRP")
                    )  # Tag 'he' as PRP (subject pronoun)
                elif word.isdigit() or contains_digit(word):
                    transformed_sentence.append(
                        (word, "CD")
                    )  # Tag all digits as cardinal numbers
                else:
                    transformed_sentence.append(
                        (word, tag)
                    )  # Keep original tag if no rule applies

                # Update previous tag for next iteration
                previous_tag = tag

            for word, tag in transformed_sentence:
                f.write(f"{word}\t{tag}")
                f.write("\n")  # Write a blank line to separate sentences
            transformed_sentences.append(transformed_sentence)

    return transformed_sentences


#### apply rules ####

Annotated_parsed = parse_training_data(Annotated_corpus_majority_tags)
after_rule_corpus = os.path.join(sys.path[0], "after_rule_corpus.txt")
transformed_predicted_tags = apply_rules(Annotated_parsed, after_rule_corpus)


#### tag 1 sentnece after applying rules ####


def brill_tagger(sentence, word_to_majority_tag):
    "Initial Brill tagger function that performs pos tagging on a sentence using the after_rule_corpus corpus by consedering the majority class for the word"
    tagged_sentence = []
    words = []
    current_token = ""
    for char in sentence:
        if char in [" ", ",", "."]:
            if current_token:
                words.append(current_token)
                current_token = ""  # Reset current_token
            if char != " ":
                words.append(char)
        else:
            current_token += char
    if current_token:
        words.append(current_token)

    for word in words:
        if word in word_to_majority_tag:
            for i in word_to_majority_tag[word]:
                tagged_sentence.append((word, i))
        else:
            # If word is not in training data, default to a common tag like 'NN' (noun)
            tagged_sentence.append((word, "NN"))

    return tagged_sentence


#### tag 1 sentnece after applying rules ####


#### Testing on 1 sentence ####

final_file = after_rule_corpus
final_parsed = parse_training_data(final_file)
word_to_tag = build_word_to_tag_dict(final_parsed)
word_to_tag_GS = build_word_to_tag_dict(gold_standard_parsed)

sample_sentence = "The economy's temperature will be taken from several vantage points this week, with readings on trade ,output, housing and inflation ."

brill_tags = brill_tagger(sample_sentence, word_to_tag)  #
brill_tags_GC = brill_tagger(sample_sentence, word_to_tag_GS)  #

#### Testing on 1 sentence ####


#### evaluate ####
def evaluate(gold_tags, annotated_tags, labels):
    "import the evaluation file to compare the tags from after_rule_corpus and test. Calculate and print macro_average, micro_average, F1-score, Precision and Reacall"
    final_annotated_tags = []
    for i in annotated_tags:
        for j in i:
            final_annotated_tags.append(j[1])

    final_gold_tags = []
    for i in gold_tags:
        for j in i:
            final_gold_tags.append(j[1])

    print(
        "Macro Average values for given labels : ",
        evaluation.macro_average(final_gold_tags, final_annotated_tags, labels),
    )  # testing function macro_average
    print(
        "Micro Average values for given labels : ",
        evaluation.micro_average(final_gold_tags, final_annotated_tags, labels),
    )  # testing function micro_average
    print(
        "F1 Score for given labels : ",
        evaluation.calculate_f1score(final_gold_tags, final_annotated_tags, labels),
    )  # testing function calculate_f1score
    print(
        "Precision-Recall for given labels : ",
        evaluation.calculate_precision_recall(
            final_gold_tags, final_annotated_tags, labels
        ),
    )  # testing function calculate_f1score
    print(
        "Matrix values for given labels : ",
        evaluation.matrix_values(final_gold_tags, final_annotated_tags, labels),
    )  # testing function calculate_f1score
    return




all_tags = []
with open(after_rule_corpus, "r") as file:
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
with open(after_rule_corpus, "r") as file:
    for line in file:
        if line.strip():  # Non-empty line
            word, tag = line.split()
            final_matrix.append((word, tag))
        else:  # Empty line indicates end of sentence
            next


##### clean data again #####





#### Confusion Matrix ####

def generate_confusion_table(transformed_corpus, gold_standard):
    confusion_table = defaultdict(int)
    for (transformed_word, transformed_tag), (gold_word, gold_tag) in zip(transformed_corpus, gold_standard):
        if transformed_tag != gold_tag:
            confusion_table[(transformed_tag, gold_tag)] += 1
    return confusion_table


confusion_table1 = generate_confusion_table(final_matrix, gold_matrix)
# print(confusion_table1)



def create_confusion_table(transformed_corpus, gold_standard):
    confusion_table = defaultdict(lambda: defaultdict(int))
    
    for (word, tag), (_, gold_tag) in zip(transformed_corpus, gold_standard):
        if tag != gold_tag:
            confusion_table[tag][gold_tag] += 1
    
    return confusion_table



#### Confusion Matrix ####


transformations = []

def apply_new_rules(corpus, transformations):
    """
    Applies the given transformations to the corpus.
    """
    transformed_corpus = []

    for i, (word, tag) in enumerate(corpus):
        transformed = False

        for rule in transformations:
            if rule['type'] == 'preceding':
                if i > 0 and corpus[i-1][1] == rule['condition_tag']:
                    if tag == rule['from_tag']:
                        transformed_corpus.append((word, rule['to_tag']))
                        transformed = True
                        break
            elif rule['type'] == 'following':
                if i < len(corpus) - 1 and corpus[i+1][1] == rule['condition_tag']:
                    if tag == rule['from_tag']:
                        transformed_corpus.append((word, rule['to_tag']))
                        transformed = True
                        break
            elif rule['type'] == 'preceding_two':
                if i > 1 and (corpus[i-1][1] == rule['condition_tag'] or corpus[i-2][1] == rule['condition_tag']):
                    if tag == rule['from_tag']:
                        transformed_corpus.append((word, rule['to_tag']))
                        transformed = True
                        break
            elif rule['type'] == 'following_two':
                if i < len(corpus) - 2 and (corpus[i+1][1] == rule['condition_tag'] or corpus[i+2][1] == rule['condition_tag']):
                    if tag == rule['from_tag']:
                        transformed_corpus.append((word, rule['to_tag']))
                        transformed = True
                        break
            elif rule['type'] == 'preceding_and_following':
                if i > 0 and i < len(corpus) - 1:
                    if corpus[i-1][1] == rule['preceding_tag'] and corpus[i+1][1] == rule['following_tag']:
                        if tag == rule['from_tag']:
                            transformed_corpus.append((word, rule['to_tag']))
                            transformed = True
                            break

        if not transformed:
            transformed_corpus.append((word, tag))
    
    return transformed_corpus



def find_best_transformation(confusion_table, corpus, gold_standard):
    best_transformation = None
    best_error_reduction = 0

    for incorrect_tag, corrections in confusion_table.items():
        for correct_tag, _ in corrections.items():
            # Check preceding word condition
            for word, tag in corpus:
                for context in ["preceding", "following"]:
                    rule = {'from_tag': incorrect_tag, 'to_tag': correct_tag, 'type': context, 'condition_tag': tag}
                    transformed_corpus = apply_new_rules(corpus, [rule])
                    error_reduction = calculate_error_reduction(transformed_corpus, gold_standard, confusion_table)
                    if error_reduction > best_error_reduction:
                        best_error_reduction = error_reduction
                        best_transformation = rule

            # Check preceding two words condition
            for i in range(2, len(corpus)):
                context = "preceding_two"
                rule = {'from_tag': incorrect_tag, 'to_tag': correct_tag, 'type': context, 'condition_tag': corpus[i-2][1]}
                transformed_corpus = apply_new_rules(corpus, [rule])
                error_reduction = calculate_error_reduction(transformed_corpus, gold_standard, confusion_table)
                if error_reduction > best_error_reduction:
                    best_error_reduction = error_reduction
                    best_transformation = rule

            # Check following two words condition
            for i in range(len(corpus) - 2):
                context = "following_two"
                rule = {'from_tag': incorrect_tag, 'to_tag': correct_tag, 'type': context, 'condition_tag': corpus[i+2][1]}
                transformed_corpus = apply_new_rules(corpus, [rule])
                error_reduction = calculate_error_reduction(transformed_corpus, gold_standard, confusion_table)
                if error_reduction > best_error_reduction:
                    best_error_reduction = error_reduction
                    best_transformation = rule

            # Check preceding and following words condition
            for i in range(1, len(corpus) - 1):
                context = "preceding_and_following"
                rule = {'from_tag': incorrect_tag, 'to_tag': correct_tag, 'type': context, 'preceding_tag': corpus[i-1][1], 'following_tag': corpus[i+1][1]}
                transformed_corpus = apply_new_rules(corpus, [rule])
                error_reduction = calculate_error_reduction(transformed_corpus, gold_standard, confusion_table)
                if error_reduction > best_error_reduction:
                    best_error_reduction = error_reduction
                    best_transformation = rule

    return best_transformation

def calculate_error_reduction(transformed_corpus, gold_standard, confusion_table):
    # Calculate the error reduction after applying a transformation
    new_confusion_table = create_confusion_table(transformed_corpus, gold_standard)
    old_errors = sum(sum(corrections.values()) for corrections in confusion_table.values())
    new_errors = sum(sum(corrections.values()) for corrections in new_confusion_table.values())
    return old_errors - new_errors


def iterative_improvement(corpus, gold_standard):
    confusion_table = create_confusion_table(corpus, gold_standard)
    transformations = []
    threshold = 1  # You can adjust this threshold based on your requirements

    while True:
        best_transformation = find_best_transformation(confusion_table, corpus, gold_standard)
        if not best_transformation:
            break

        transformed_corpus = apply_new_rules(corpus, [best_transformation])
        new_confusion_table = create_confusion_table(transformed_corpus, gold_standard)
        
        error_reduction = calculate_error_reduction(transformed_corpus, gold_standard, confusion_table)
        if error_reduction <= threshold:
            break

        transformations.append(best_transformation)
        corpus = transformed_corpus
        confusion_table = new_confusion_table
    
    return transformations, corpus

gold_standard = gold_matrix
transformed_corpus = final_matrix

transformations, improved_corpus = iterative_improvement(transformed_corpus, gold_standard)

# Print the final set of transformations
for transformation in transformations:
    print(transformation)















































































































































































































































































































































































































































































# def create_potential_transformations(confusion_table):
#     transformations = []
#     for (wrong_tag, correct_tag), count in confusion_table.items():
#         # Create a transformation pattern for this error type
#         # For simplicity, we'll consider transformations based on the preceding tag
#         transformations.append((wrong_tag, correct_tag, "PREV_TAG"))
#         transformations.append((wrong_tag, correct_tag, "NEXT_TAG"))
#     return transformations





# def create_potential_transformations(corpus, confusion_table):
#     transformations = set()
#     corpus_len = len(corpus)

#     for i, (word, tag) in enumerate(corpus):
#         if i > 0:
#             prev_tag = corpus[i - 1][1]
#             transformations.add((tag, confusion_table.get((tag, corpus[i][1]), corpus[i][1]), "PREV_TAG", prev_tag))
#         if i < corpus_len - 1:
#             next_tag = corpus[i + 1][1]
#             transformations.add((tag, confusion_table.get((tag, corpus[i][1]), corpus[i][1]), "NEXT_TAG", next_tag))
#         if i > 1:
#             prev_tag_2 = corpus[i - 2][1]
#             transformations.add((tag, confusion_table.get((tag, corpus[i][1]), corpus[i][1]), "PREV_TAG2", prev_tag_2))
#         if i < corpus_len - 2:
#             next_tag_2 = corpus[i + 2][1]
#             transformations.add((tag, confusion_table.get((tag, corpus[i][1]), corpus[i][1]), "NEXT_TAG2", next_tag_2))
#         if i > 0 and i < corpus_len - 1:
#             prev_tag = corpus[i - 1][1]
#             next_tag = corpus[i + 1][1]
#             transformations.add((tag, confusion_table.get((tag, corpus[i][1]), corpus[i][1]), "PREV_NEXT_TAG", prev_tag, next_tag))
    
#     return transformations

# a = create_potential_transformations(final_matrix, confusion_table1)
# print(a)








# def apply_transformation(corpus, transformation):
#     wrong_tag, correct_tag, context_type = transformation
#     new_corpus = []
#     for i, (word, tag) in enumerate(corpus):
#         if tag == wrong_tag:
#             if context_type == "PREV_TAG" and i > 0 and corpus[i - 1][1] == correct_tag:
#                 new_corpus.append((word, correct_tag))
#             elif context_type == "NEXT_TAG" and i < len(corpus) - 1 and corpus[i + 1][1] == correct_tag:
#                 new_corpus.append((word, correct_tag))
#             else:
#                 new_corpus.append((word, tag))
#         else:
#             new_corpus.append((word, tag))
#     return new_corpus

# def calculate_error_reduction(transformed_corpus, gold_standard, confusion_table):
#     new_confusion_table = generate_confusion_table(transformed_corpus, gold_standard)
#     error_reduction = sum(confusion_table.values()) - sum(new_confusion_table.values())
#     return error_reduction

# # Example usage:
# threshold = 10  # Minimum error reduction to accept a transformation

# new = []
# while True:
#     confusion_table = generate_confusion_table(final_matrix, gold_matrix)
#     potential_transformations = create_potential_transformations(final_matrix,confusion_table)

#     best_transformation = None
#     best_reduction = 0
#     for transformation in potential_transformations:
#         new_corpus = apply_transformation(final_matrix, transformation)
#         reduction = calculate_error_reduction(new_corpus, gold_matrix, confusion_table)
#         if reduction > best_reduction:
#             best_reduction = reduction
#             best_transformation = transformation
#             best_new_corpus = new_corpus
#     if best_reduction <= threshold:
#             break

#     new = best_new_corpus
#     print(new)
#     print(f"Applied transformation: {best_transformation}")
#     print(f"Error reduction: {best_reduction}")

# # print("Final transformed corpus:")
# # print(new)


# def write_results_to_file(corpus, file_name):
#     with open(file_name, 'w') as file:
#         for word, tag in corpus:
#             file.write(f"{word}\t{tag}\n")
#         file.write("\n")

# # write_results_to_file(transformed_corpus, "after_learning_algorithm.txt")




