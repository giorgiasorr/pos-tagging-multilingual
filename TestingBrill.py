# # # Sample tagged data (word, tag) pairs
# # training_data = [
# #     ("The", "DT"), ("dog", "NN"), ("barks", "VBZ"), ("loudly", "RB"),
# #     ("A", "DT"), ("cat", "NN"), ("meows", "VBZ"), ("softly", "RB")
# # ]

# # # Test data for evaluation
# # test_data = [
# #     ("The", "DT"), ("cat", "NN"), ("barks", "VBZ"), ("loudly", "RB")
# # ]


# # # Transformation rules (template, source_tag, target_tag)
# # transformation_rules = [
# #     (1, "NN", "VBZ"),  # If NN, transform to VBZ
# #     (2, "NN", "RB"),   # If NN, transform to RB
# #     (3, "DT", "JJ")    # If DT, transform to JJ
# # ]


# # def apply_transformation_rules(sentence, rules):
# #     # Apply transformation rules to a tagged sentence
# #     tagged_sentence = []
# #     for word, tag in sentence:
# #         for rule in rules:
# #             template, source_tag, target_tag = rule
# #             if tag == source_tag:
# #                 tag = target_tag
# #         tagged_sentence.append((word, tag))
# #     return tagged_sentence

# # def brill_tagger(training_data, test_data, rules):
# #     tagged_sentences = []
    
# #     # Apply transformation rules to training data
# #     for sentence in training_data:
# #         tagged_sentences.append(apply_transformation_rules(sentence, rules))
    
# #     # Evaluate on test data
# #     correct_count = 0
# #     total_count = len(test_data)
    
# #     for i in range(len(test_data)):
# #         expected_tag = test_data[i]
# #         predicted_tag = tagged_sentences[i][i]
        
# #         if expected_tag == predicted_tag:
# #             correct_count += 1
    
# #     accuracy = (correct_count / total_count) * 100
# #     return accuracy

# # # Test the Brill Tagger
# # accuracy = brill_tagger([training_data], [test_data], transformation_rules)
# # print(f"Accuracy: {accuracy:.2f}%")



























# # # # from collections import defaultdict


# # # # # A class to hold the information about the tuples
# # # # class TaggerTuple:
# # # #     def __init__(self, from_tag, to_tag, pre_tag, score):
# # # #         self.from_tag = from_tag
# # # #         self.to_tag = to_tag
# # # #         self.pre_tag = pre_tag
# # # #         self.score = score


# # # # # A function to store the given corpus into string
# # # # def read_file(filename):
# # # #     corpus_line = ""

# # # #     with open(filename) as file:
# # # #         for line in file:
# # # #             corpus_line = corpus_line + line
# # # #     file.close()

# # # #     return corpus_line


# # # # # Tokenize input file and create a unigram model
# # # # def tokenize(corpus_line):
# # # #     unigram = defaultdict(dict)
# # # #     unigram_tokens = {}

# # # #     unigram_file = open("output\\unigram\\unigram.txt", "w")
# # # #     unigram_tokens_file = open("output\\unigram\\unigram_tokens.txt", "w")

# # # #     for word in corpus_line.split():
# # # #         words = word.split("_")

# # # #         if words[0] in unigram:
# # # #             if words[1] in unigram[words[0]]:
# # # #                 unigram[words[0]][words[1]] = unigram[words[0]][words[1]] + 1
# # # #             else:
# # # #                 unigram[words[0]][words[1]] = 1
# # # #         else:
# # # #             unigram[words[0]][words[1]] = 1

# # # #         if words[0] in unigram_tokens:
# # # #             unigram_tokens[words[0]] = unigram_tokens[words[0]] + 1
# # # #         else:
# # # #             unigram_tokens[words[0]] = 1

# # # #     for key, value in unigram.items():
# # # #         unigram_file.write(key + " " + str(value) + "\n")
# # # #     unigram_file.close()

# # # #     for key, value in unigram_tokens.items():
# # # #         unigram_tokens_file.write(key + " " + str(value) + "\n")
# # # #     unigram_tokens_file.close()

# # # #     return unigram


# # # # # Initialize the dummy corpus with mostly like tags
# # # # def initialize_with_most_likely_tag():
# # # #     most_likely_unigram = {}

# # # #     with open("output\\unigram\most_probable_unigram.txt", "w") as most_likely_unigram_file:
# # # #         for key, value in unigram.items():
# # # #             sorted_list = sorted(value, key=value.get, reverse=True)
# # # #             most_likely_unigram[key] = sorted_list[0]
# # # #             most_likely_unigram_file.write(key + " " + str(sorted_list[0]) + "\n")
# # # #     most_likely_unigram_file.close()

# # # #     return most_likely_unigram


# # # # # Train the model to generate 10 transformational templates
# # # # def tbl(most_likely_unigram, corpus_tuple, current_tag):
# # # #     n = 1
# # # #     transforms_queue = []

# # # #     while n <= 10:
# # # #         best_transform = get_best_transform(most_likely_unigram, corpus_tuple, correct_tag, current_tag, n)

# # # #         if best_transform.from_tag == '' and best_transform.to_tag == '':
# # # #             break

# # # #         apply_transform(best_transform, corpus_tuple, current_tag, n)
# # # #         transforms_queue.append(best_transform)
# # # #         n = n + 1

# # # #     return transforms_queue


# # # # # A function to get the best transform
# # # # def get_best_transform(most_likely_unigram, corpus_tuple, correct_tag, current_tag, n):
# # # #     instance = get_best_instance(most_likely_unigram, corpus_tuple, correct_tag, current_tag, n)
# # # #     return instance


# # # # # A function to get the best instance
# # # # def get_best_instance(most_likely_unigram, corpus_tuple, correct_tag, current_tag, iteration):
# # # #     best_score = 0
# # # #     all_tags = ["NN", "VB"]

# # # #     transform = TaggerTuple("", "", "", "")

# # # #     print("Iteration :: " + str(iteration))

# # # #     for from_tag in all_tags:
# # # #         for to_tag in all_tags:
# # # #             max_difference = 0
# # # #             num_good_transform = {}
# # # #             num_bad_transform = {}

# # # #             if from_tag == to_tag:
# # # #                 continue

# # # #             for pos in range(1, len(corpus_tuple)):

# # # #                 if to_tag == correct_tag[pos] and from_tag == current_tag[pos]:
# # # #                     rule = (current_tag[pos - 1], from_tag, to_tag)

# # # #                     if rule in num_good_transform:
# # # #                         num_good_transform[rule] += 1
# # # #                     else:
# # # #                         num_good_transform[rule] = 1
# # # #                 elif from_tag == correct_tag[pos] and from_tag == current_tag[pos]:
# # # #                     rule = (current_tag[pos - 1], from_tag, to_tag)

# # # #                     if rule in num_bad_transform:
# # # #                         num_bad_transform[rule] += 1
# # # #                     else:
# # # #                         num_bad_transform[rule] = 1

# # # #             for key, value in num_good_transform.items():
# # # #                 if key in num_bad_transform:
# # # #                     difference = num_good_transform[key] - num_bad_transform[key]
# # # #                 else:
# # # #                     difference = num_good_transform[key]

# # # #                 if difference > max_difference:
# # # #                     arg_max = key[0]
# # # #                     max_difference = difference

# # # #             if max_difference > best_score:
# # # #                 best_rule = "Change tag FROM :: '" + from_tag + "' TO :: '" + to_tag + "' PREV tag :: '" + arg_max + "'"
# # # #                 best_score = max_difference

# # # #                 print("Best Rule :: " + best_rule)
# # # #                 transform = TaggerTuple(from_tag, to_tag, arg_max, best_score)

# # # #     return transform


# # # # # Apply transform after calculating best score of transformation template
# # # # def apply_transform(best_transform, corpus_tuple, current_tag, n):
# # # #     current_tag_File = open("output\logs\iteration_" + str(n) + ".txt", "w")

# # # #     for pos in range(1, len(corpus_tuple)):
# # # #         if (current_tag[pos] == best_transform.from_tag) and (current_tag[pos - 1] == best_transform.pre_tag):
# # # #             current_tag[pos] = best_transform.to_tag

# # # #     for pos in range(0, len(current_tag)):
# # # #         current_tag_File.write(current_tag[pos] + "\n")


# # # # # Divide the corpus into 3 forms
# # # # # corpus_tuple : all the corpus words
# # # # # correct_tag :  all the corpus tags
# # # # # current_tag_File : most likely tag applied to all the words in corpus
# # # # def create_corpus_tuple(corpus_line, most_likely_unigram):
# # # #     corpus_tuple = []
# # # #     correct_tag = []
# # # #     current_tag = []

# # # #     corpus_tuple_file = open("output\\tuple\corpus_tuple.txt", "w")
# # # #     correct_tag_file = open("output\\tags\correct_tag.txt", "w")
# # # #     current_tag_file = open("output\\tags\current_tag.txt", "w")

# # # #     for word in corpus_line.split():
# # # #         words = word.split("_")

# # # #         corpus_tuple.append(words[0])
# # # #         correct_tag.append(words[1])
# # # #         current_tag.append(most_likely_unigram[words[0]])

# # # #         corpus_tuple_file.write(words[0] + "\n")
# # # #         correct_tag_file.write(words[1] + "\n")
# # # #         current_tag_file.write(most_likely_unigram[words[0]] + "\n")

# # # #     return corpus_tuple, correct_tag, current_tag


# # # # # sort all the transformation generated in oprder of their score
# # # # def sort_transformation_in_order_of_score(transformation_transforms_queue):
# # # #     sorted_Templates = sorted(transformation_transforms_queue, key=lambda x: x.score, reverse=True)
# # # #     index = 1

# # # #     with open("output\\top10.txt", "w") as top10_file:
# # # #         for transformation in sorted_Templates:
# # # #             result = str(index) + ":: From '" + transformation.from_tag + "' To '" + transformation.to_tag\
# # # #                      + "' when Prev '" + transformation.pre_tag + "'"
# # # #             print(result)
# # # #             top10_file.write(result + "\n")
# # # #             index = index + 1
# # # #     top10_file.close()

# # # #     return sorted_Templates


# # # # filename = "/Users/mayurideshmukh/Desktop/Team-Lab/data/train.col"

# # # # corpus_line = read_file(filename)
# # # # unigram = tokenize(corpus_line)

# # # # most_likely_unigram = initialize_with_most_likely_tag()
# # # # corpus_tuple, correct_tag, current_tag = create_corpus_tuple(corpus_line, most_likely_unigram)
# # # # transformation_transforms_queue = tbl(most_likely_unigram, corpus_tuple, current_tag)

# # # # print("\n================== Top 10 Rules ==================")
# # # # sorted_Templates = sort_transformation_in_order_of_score(transformation_transforms_queue)














































# # class BrillTagger:
# #     def __init__(self, initial_tagger, templates):
# #         self.initial_tagger = initial_tagger  # Initial tagger to provide baseline tagging
# #         self.templates = templates  # Transformation templates

# #     def train(self, tagged_sentences, max_iterations=5):
# #         for _ in range(max_iterations):
# #             self.apply_templates(tagged_sentences)

# #     def apply_templates(self, tagged_sentences):
# #         for sentence in tagged_sentences:
# #             words, gold_tags = zip(*sentence)
# #             predicted_tags = self.initial_tagger.tag(words)
# #             for i in range(len(words)):
# #                 if predicted_tags[i] != gold_tags[i]:
# #                     self.update_templates(words, i, predicted_tags, gold_tags)

# #     def update_templates(self, words, index, predicted_tags, gold_tags):
# #         # Apply transformation templates to update the model
# #         # You can implement specific transformation logic here
# #         pass

# #     def tag(self, words):
# #         return self.initial_tagger.tag(words)  # Use initial tagger for tagging

# #     def evaluate(self, tagged_sentences):
# #         # Evaluate the performance of the Brill Tagger
# #         # This can be implemented based on accuracy or other metrics
# #         pass



# # def transformation_template(word, index, predicted_tags, gold_tags):
# #     if index > 0 and predicted_tags[index-1] == 'NN' and gold_tags[index] == 'VB':
# #         # Rule: If the previous word was tagged as 'NN' and current word should be 'VB', correct it
# #         predicted_tags[index] = 'VB'
# #     return predicted_tags


# # # Example usage

# # # Define a simple initial tagger (e.g., rule-based or default tagger)
# # class DefaultTagger:
# #     def tag(self, words):
# #         return ['NN'] * len(words)  # Default tagging as 'NN'

# # # Example transformation templates
# # templates = [transformation_template]

# # # Initialize Brill Tagger
# # initial_tagger = DefaultTagger()
# # brill_tagger = BrillTagger(initial_tagger, templates)

# # # Example tagged sentences for training
# # tagged_sentences = [
# #     [("The", "DT"), ("cat", "NN"), ("is", "VBZ"), ("on", "IN"), ("the", "DT"), ("mat", "NN")],
# #     [("A", "DT"), ("dog", "NN"), ("chases", "VBZ"), ("the", "DT"), ("cat", "NN")]
# # ]

# # # Train the Brill Tagger
# # brill_tagger.train(tagged_sentences)

# # # Test the Brill Tagger
# # test_sentence = ["The", "dog", "is", "on", "the", "mat"]
# # print(brill_tagger.tag(test_sentence))
































# # class BrillTagger:
# #     def __init__(self, initial_tagger, templates):
# #         self.initial_tagger = initial_tagger  # Initial tagger to provide baseline tagging
# #         self.templates = templates  # Transformation templates

# #     def train(self, tagged_sentences, max_iterations=5):
# #         for _ in range(max_iterations):
# #             for sentence in tagged_sentences:
# #                 words, gold_tags = zip(*sentence)
# #                 predicted_tags = self.initial_tagger.tag(words)
# #                 self.apply_templates(words, predicted_tags, gold_tags)

# #     def apply_templates(self, words, predicted_tags, gold_tags):
# #         for i in range(len(words)):
# #             if predicted_tags[i] != gold_tags[i]:
# #                 predicted_tags = self.update_tags_with_templates(words, i, predicted_tags, gold_tags)
# #         return predicted_tags

# #     def update_tags_with_templates(self, words, index, predicted_tags, gold_tags):
# #         for template in self.templates:
# #             updated_tags = template(words, index, predicted_tags, gold_tags)
# #             if updated_tags is not None and updated_tags != predicted_tags:
# #                 return updated_tags
# #         return predicted_tags

# #     def tag(self, words):
# #         return self.initial_tagger.tag(words)  # Use initial tagger for tagging

# # # Example transformation template function
# # def transformation_template(words, index, predicted_tags, gold_tags):
# #     if index > 0 and predicted_tags[index-1] == 'NN' and gold_tags[index] == 'VB':
# #         # Rule: If the previous word was tagged as 'NN' and current word should be 'VB', correct it
# #         predicted_tags = list(predicted_tags)  # Convert to list to modify
# #         predicted_tags[index] = 'VB'
# #         return predicted_tags
# #     return None  # No changes made

# # # Example usage
# # class DefaultTagger:
# #     def tag(self, words):
# #         tagged_words = []
# #         for word in words:
# #             if word.lower() in ['is', 'am', 'are', 'was', 'were']:
# #                 tagged_words.append('VB')  # Verb
# #             elif word.lower() in ['the', 'a', 'an']:
# #                 tagged_words.append('DT')  # Determiner
# #             else:
# #                 tagged_words.append('NN')  # Noun (default)
# #         return tagged_words


# # # Initialize Brill Tagger
# # initial_tagger = DefaultTagger()
# # templates = [transformation_template]
# # brill_tagger = BrillTagger(initial_tagger, templates)

# # # Example tagged sentences for training
# # tagged_sentences = [
# #     [("The", "DT"), ("cat", "NN"), ("is", "VBZ"), ("on", "IN"), ("the", "DT"), ("mat", "NN")],
# #     [("A", "DT"), ("dog", "NN"), ("chases", "VBZ"), ("the", "DT"), ("cat", "NN")]
# # ]

# # # Train the Brill Tagger
# # brill_tagger.train(tagged_sentences)

# # # Test the Brill Tagger
# # test_sentence = ["The", "dog", "is", "on", "the", "mat"]
# # predicted_tags = brill_tagger.tag(test_sentence)
# # print(test_sentence)
# # print(predicted_tags)

















































# # train_file = '/Users/mayurideshmukh/Desktop/Team-Lab/data/train.col'
# # dev_predicted_file = '/Users/mayurideshmukh/Desktop/Team-Lab/data/dev-predicted.col'

# # def build_word_to_tag_dict(training_file):
# #     word_to_tag = {}
    
# #     with open(training_file, 'r') as file:
# #         for line in file:
# #             if line.strip():  # Skip empty lines
# #                 word, tag = line.split()
# #                 if word not in word_to_tag:
# #                     word_to_tag[word] = {}
# #                 if tag in word_to_tag[word]:
# #                     word_to_tag[word][tag] += 1
# #                 else:
# #                     word_to_tag[word][tag] = 1
    
# #     return word_to_tag

# # # print(build_word_to_tag_dict(train_file))


# # def calculate_majority_class(word_to_tag):
    
# #     word_to_majority_tag = {}
    
# #     for word, tag_counts in word_to_tag.items():
# #         majority_tag = max(tag_counts, key=tag_counts.get)
# #         word_to_majority_tag[word] = majority_tag
    
# #     return word_to_majority_tag


# # # a=build_word_to_tag_dict(train_file)
# # # print(calculate_majority_class(a))


# # def initial_tagger(sentence, word_to_majority_tag):
# #     tagged_sentence = []
# #     words = sentence.split()
    
# #     for word in words:
# #         if word in word_to_majority_tag:
# #             tagged_sentence.append((word, word_to_majority_tag[word]))
# #         else:
# #             # If word is not in training data, default to a common tag like 'NN' (noun)
# #             tagged_sentence.append((word, 'NN'))
    
# #     return tagged_sentence

# # a=build_word_to_tag_dict(train_file)
# # a1=build_word_to_tag_dict(dev_predicted_file)
# # b=calculate_majority_class(a)
# # b1=calculate_majority_class(a1)
# # sample_sentence = "In an Oct. 19 review of "
# # c = initial_tagger(sample_sentence, b)
# # c1 = initial_tagger(sample_sentence, b1)


# # def detect_errors(predicted_tags, gold_standard_tags):
# #     errors = []

# #     # Iterate over each sentence in predicted_tags
# #     for predicted_sentence in predicted_tags:
# #         matched_sentence = None
# #         min_distance = float('inf')

# #         # Find the most similar sentence in gold_standard_tags
# #         for gold_sentence in gold_standard_tags:
# #             # Calculate similarity (e.g., based on word order or content)
# #             # Here, we'll use a simple word overlap approach
# #             predicted_words = [word for word, _ in predicted_sentence]
# #             gold_words = [word for word, _ in gold_sentence]
# #             similarity = len(set(predicted_words) & set(gold_words))

# #             if similarity > 0 and similarity < min_distance:
# #                 min_distance = similarity
# #                 matched_sentence = gold_sentence
        
# #         # Compare predicted tags with matched gold standard tags
# #         if matched_sentence:
# #             for i, (predicted_word, predicted_tag) in enumerate(predicted_sentence):
# #                 if i < len(matched_sentence):
# #                     _, gold_tag = matched_sentence[i]
# #                     if predicted_tag != gold_tag:
# #                         errors.append((predicted_word, predicted_tag, gold_tag))
# #         else:
# #             # No match found for this predicted sentence
# #             # Consider all tags as errors (assuming misalignment)
# #             for predicted_word, predicted_tag in predicted_sentence:
# #                 errors.append((predicted_word, predicted_tag, None))  # None indicates no gold standard tag
    
# #     return errors

# # print(detect_errors(c,c1))



































# from nltk import pos_tag
# from nltk.tokenize import word_tokenize

# # Example sentence
# sentence = "The cat is sitting on the mat."

# # Tokenize and POS tag
# tokens = word_tokenize(sentence)
# tagged = pos_tag(tokens)

# print(tagged)


# import spacy

# # Load English tokenizer, tagger, parser, NER, and word vectors
# nlp = spacy.load("en_core_web_sm")

# # Process a sentence
# doc = nlp("The cat is sitting on the mat.")

# # Analyze syntactic dependencies
# for token in doc:
#     print(token.text, token.pos_, token.dep_)


# from spacy.matcher import Matcher

# matcher = Matcher(nlp.vocab)
# pattern = [{"POS": "NOUN"}, {"LOWER": "is"}, {"POS": "VERB"}]

# matcher.add("is_action", [pattern])

# matches = matcher(doc)
# for match_id, start, end in matches:
#     print("Match found:", doc[start:end].text)



# def assign_pos_tag(word):
#     # Check if the word ends with the suffix '-ing' (case insensitive)
#     if word.lower().endswith('ing'):
#         return (word, 'NN')  # Label the word as a noun (NN) if it ends with '-ing'
#     else:
#         return (word, None)  # Return None for the tag if no specific condition is met

# # Example usage:
# words = ['walking', 'eating', 'play', 'running']

# transformed_sentence = []
# for word in words:
#     word, tag = assign_pos_tag(word)
#     transformed_sentence.append((word, tag))

# print(transformed_sentence)







# def contains_digit(s):
#     isdigit = str.isdigit
#     return any(map(isdigit,s))


# print(contains_digit("400th"))









# non_blank_count = 0

# with open('/Users/mayurideshmukh/Desktop/Team-Lab/data/dev-predicted.col') as infp:
#     for line in infp:
#        if line.strip():
#           non_blank_count += 1

# print ('number of non-blank lines found %d' % non_blank_count)



# from nltk.tag import BrillTagger

# print(BrillTagger.rules())





















































import numpy as np
from sklearn.metrics import multilabel_confusion_matrix
import collections


########## Read file from IMS #########
devList = []
with open("/Users/mayurideshmukh/Desktop/Team-Lab/data/dev.col", "r") as file: 
    for i in (file):
        line = i.strip()
        if line:
            devList.append(line)


only_tags = []
for i in devList:
    only_tags.append(i.split()[1])


print(only_tags)
















def apply_transformational_rules(sentences):
    transformed_sentences = []

    for sentence in sentences:
        transformed_sentence = []
        previous_tag = None
        
        for i, (word, tag) in enumerate(sentence):
            # Apply transformational rules based on context
            if word == 'continued' and i < len(sentence) - 1 and (sentence[i + 1][1] == 'NN' or sentence[i + 1][1] == 'VBG' ):
                transformed_sentence.append(('continued', 'VBN'))  # 'all' before a DT is likely a predeterminer 
            # elif word.endswith('ing') :
            #         transformed_sentence.append((word, 'VBG'))   
            # elif word.isalpha() and previous_tag == None :
            #     if word.endswith('s'):
            #         transformed_sentence.append((word, 'NNPS'))  # 'all' before a DT is likely a predeterminer     
            #     else:
            #         transformed_sentence.append((word, 'NNP'))  # 'all' before a DT is likely a predeterminer
            elif tag == 'NN':
                # Rule: NN --> VBP if the preceding tag is 'PRP'
                if i > 0 and sentence[i - 1][1] == 'PRP':
                    transformed_sentence.append((word, 'VBP'))
                # Rule: NN --> JJ if the following tag is 'JJ'
                elif i + 1 < len(sentence) and sentence[i + 1][1] == 'JJ':
                    transformed_sentence.append((word, 'JJ'))
                # Rule: NN --> IN if the preceding tag is '.'
                elif i > 0 and sentence[i - 1][1] == '.':
                    transformed_sentence.append((word, 'IN'))
                else:
                    transformed_sentence.append((word, tag))  # Keep original tag if no rule applies
            elif tag == 'NNP':
                # Rule: NNP --> NN if the tag of words i-3...i-1 is JJ
                if i >= 3 and all(sent[i - j][1] == 'JJ' for j in range(1, 4)):
                    transformed_sentence.append((word, 'NN'))
                # Rule: NNP --> NNP if the tag of words i+1...i+2 is NNP
                elif i + 2 < len(sentence) and all(sent[i + j][1] == 'NNP' for j in range(1, 3)):
                    transformed_sentence.append((word, 'NNP'))
                else:
                    transformed_sentence.append((word, tag))  # Keep original tag if no rule applies
            elif previous_tag == 'LS' and word == '-':
                    transformed_sentence.append(('-', 'HYPH'))   
            elif word == '-':
                    transformed_sentence.append(('-', 'HYPH'))
            elif word == '#':
                    transformed_sentence.append(('#', '$'))
            elif word == 'Farmers':
                if previous_tag == 'WRB':
                    transformed_sentence.append(('Farmers', 'NNP'))    
                else:
                    transformed_sentence.append(('Farmers', 'NNPS'))
            elif word == '{':
                transformed_sentence.append(('{', '-LRB-'))
            elif word == '}':
                transformed_sentence.append(('}', '-RRB-'))
            elif word == '/':
                transformed_sentence.append(('/', 'SYM'))
            elif word == 'to':
                # Determine tag for 'to' based on previous tag
                ptags = ['VB', 'VBP', 'MD',  'NN', 'JJ', 'NNS', 'RB', 'VBZ', 'VBD']
                if previous_tag in ptags and (sentence[i + 1][1] == 'VB' or sentence[i + 1][1] == 'VBZ' or sentence[i + 1][1] == 'VBD'  ):
                    transformed_sentence.append(('to', 'TO'))  # Tag 'to' as infinitive marker preposition if next tag is verb
                elif previous_tag in ptags and (sentence[i + 1][1] == 'DT' or sentence[i +1][1] ==  'NN') and sentence[i +2][1] not in ['VB', 'VBZ', 'VBD']:
                    transformed_sentence.append(('to', 'IN'))  # Tag 'to' as infinitive marker preposition if next tag is verb
                else:
                    transformed_sentence.append(('to', 'TO'))  # Otherwise, tag 'to' as ipreposition
            elif word == 'all' and i < len(sentence) - 1 and (sentence[i + 1][1] == 'DT' or sentence[i + 1][1] == 'PRP$' ):
                transformed_sentence.append(('all', 'PDT'))  # 'all' before a DT is likely a predeterminer
            elif word.isdigit() or contains_digit(word) :
                transformed_sentence.append((word, 'CD'))  # Tag all digits as cardinal numbers
            
            else:
                transformed_sentence.append((word, tag))  # Keep original tag if no rule applies
            
            # Update previous tag for next iteration
            previous_tag = tag
        
        transformed_sentences.append(transformed_sentence)

    return transformed_sentences








# transformed_predicted_tags = apply_transformational_rules(predicted_parsed)