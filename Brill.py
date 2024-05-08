import evaluation # type: ignore


def contains_digit(s):
    isdigit = str.isdigit
    return any(map(isdigit,s))


###   [[('the', 'DT), ('apple', 'NN'...)],[],[]]

train_file = "/Users/mayurideshmukh/Desktop/Team-Lab/data/dev-predicted.col"
gold_standard_file = "/Users/mayurideshmukh/Desktop/Team-Lab/data/dev.col"


def parse_training_data(training_file):
    sentences = []
    current_sentence = []

    with open(training_file, 'r') as file:
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

def build_word_to_tag_dict(sentences):
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


def calculate_majority_class(word_to_tag):
    word_to_majority_tag = {}

    for word, tag_counts in word_to_tag.items():
        majority_tag = max(tag_counts, key=tag_counts.get)
        word_to_majority_tag[word] = majority_tag

    return word_to_majority_tag

def initial_tagger(sentence, word_to_majority_tag):
    tagged_sentence = []
    words = sentence.split()
    
    for word in words:
        if word in word_to_majority_tag:
            tagged_sentence.append((word, word_to_majority_tag[word]))
        else:
            # If word is not in training data, default to a common tag like 'NN' (noun)
            tagged_sentence.append((word, 'NN'))
    
    return tagged_sentence

# sample_sentence = "In an Oct. 19 review of "
# initial_tags = initial_tagger(sample_sentence, word_to_majority_tag)
# print(initial_tags)

predicted_parsed = parse_training_data(train_file)
gold_standard_parsed=parse_training_data(gold_standard_file)
# print(a)
# print(build_word_to_tag_dict(a))





def detect_errors(predicted_tags, gold_standard_tags):
    errors = []

    # Iterate over sentences
    for predicted_sentence, gold_sentence in zip(predicted_tags, gold_standard_tags):
        assert len(predicted_sentence) == len(gold_sentence), "Sentence length mismatch"
        
        # Compare predicted tags with gold standard tags
        for (predicted_word, predicted_tag), (gold_word, gold_tag) in zip(predicted_sentence, gold_sentence):
            if predicted_tag != gold_tag:
                errors.append((predicted_word, predicted_tag, gold_tag))

    return errors

# # Example usage:
# predicted_tags = [  # Example predicted tags
#     [('The', 'DT'), ('bonds', 'NNS'), ('go', 'VBP'), ('on', 'IN'), ('sale', 'NN'), ('Oct.', 'NNP'), ('19', 'CD'), ('.', '.')],
#     [('The', 'DT'), ('debate', 'NN'), ('over', 'IN'), ('National', 'NNP'), ('Service', 'NNP'), ('has', 'VBZ'), ('begun', 'VBN'), ('again', 'RB'), ('.', '.')]
# ]

# gold_standard_tags = [  # Example gold standard tags
#     [('The', 'DT'), ('bonds', 'NNS'), ('go', 'VB'), ('on', 'IN'), ('sale', 'NN'), ('Oct.', 'NNP'), ('19', 'CD'), ('.', '.')],
#     [('The', 'DT'), ('debate', 'NN'), ('over', 'IN'), ('National', 'NNP'), ('Service', 'NNP'), ('has', 'VBZ'), ('begun', 'VBN'), ('again', 'RB'), ('.', '.')]
# ]

# # Perform error detection
# errors = detect_errors(predicted_parsed, gold_standard_parsed)

# # Print detected errors
# for error in errors:
#     print(f"Error: Predicted tag '{error[1]}' for word '{error[0]}' is incorrect; gold standard tag is '{error[2]}'")

# print(len(errors))



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

transformed_predicted_tags = apply_transformational_rules(predicted_parsed) # test_parse
#store = []
# compare 

# # Print corrected sentences after applying rules
# print("\nCorrected Sentences:")
# for sentence in transformed_predicted_tags:
#     print(sentence)

# print(len(transformed_predicted_tags))


errors = detect_errors(transformed_predicted_tags, gold_standard_parsed)

error_word = []
# Print detected errors
for error in errors:
    # print(f"Error: Predicted tag '{error[1]}' for word '{error[0]}' is incorrect; gold standard tag is '{error[2]}'")
    error_word.append(error[0])
#     if error[0] == '-':
#         print (error[0], error[1], error[2])

    
    
from collections import Counter
# list1=['apple','egg','apple','banana','egg','apple']
counts = Counter(error_word)
# print(counts)
# print(len(errors))








# print(transformed_predicted_tags)

only_transformed_tags = []
for i in transformed_predicted_tags:
    for j,k in i:
        only_transformed_tags.append(k)
            
# print(only_transformed_tags)






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


only_true_tags = []
for i in devList:
    only_true_tags.append(i.split()[1])


# print(only_true_tags)




tag = ["NN","VB","DT","TO"]

# print(evaluation.macro_average(only_true_tags,only_transformed_tags,tag))
# print(evaluation.calculate_f1score(only_true_tags,only_transformed_tags,tag))

































