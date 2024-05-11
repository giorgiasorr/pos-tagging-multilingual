# import numpy as np
# from sklearn.metrics import multilabel_confusion_matrix
import collections


########### Read file from IMS #########
# devList = []
# with open("/Users/mayurideshmukh/Desktop/Team-Lab/data/train.col", "r") as file: 
#     for i in (file):
#         line = i.strip()
#         devList.append(line)




# ######### put it in Dict to make it more usable ##############
# devDict = {}
# for i in devList:
#     try:
#         if i.split()[1] not in devDict:
#             devDict[i.split()[1]] = [i.split()[0]]   # tags are keys and words are values
#         else :
#             if (i.split()[0]) in devDict[i.split()[1]]: # Remove duplicate values # maybe need to keep the duplicates ???
#                 continue
#             else:
#                 devDict[i.split()[1]].append(i.split()[0])  # append values of same tag in a list
#     except IndexError:
#         continue

# print(devDict)



# print(devDict)



######## Take input ###########
# sentence = input("Enter a sentence : ")
# print(sentence.split())
# for i in sentence.split():
#     for tags, words in devDict.items():
#         for word in words:
#             if word == i:
#                 print(i, ":",tags)












































# # ######### test with libs #########
# # # y_true = ["DT", "NN", "POS", "NN", "MD", "VB","VBN", "IN", "JJ", "NN", "NNS", "DT"]
# # # y_pred = ["DT", "MD", "POS", "MD", "NN", "VB","NN", "IN", "JJ", "NN", "NNS", "NNS"]
# # # print(multilabel_confusion_matrix(y_true, y_pred,labels=["DT", "NN", "NNS"]))


# # # y_true = ["NN", "DT", "P", "HYP"]
# # # y_pred = ["NN", "VB", "P", "P"]
# # # print(multilabel_confusion_matrix(y_true, y_pred,labels=["NN"]))

# # # label=["P"]
# # # if len(y_true) == len(y_pred):
# # #     tp = multilabel_confusion_matrix(y_true, y_pred,labels=label)[0][0][0]
# # #     tn = multilabel_confusion_matrix(y_true, y_pred,labels=label)[0][1][1]
# # #     fp = multilabel_confusion_matrix(y_true, y_pred,labels=label)[0][0][1]
# # #     fn = multilabel_confusion_matrix(y_true, y_pred,labels=label)[0][1][0]
# # #     print(tp,fp,fn,tn)

# # # Precision = tp/(tp+fp)
# # # Recall = tp/(tp+fn)
# # # F1Score= 2*(Precision*Recall)/(Precision + Recall)
# # # print("Precision of Tag", label, ":",Precision)
# # # print("Recall of Tag", label, ":",Recall)
# # # print("F1Score of Tag", label, ":",F1Score)


 
























# # ########## evaluation logic ###########


# # y_true = ["NN", "DT", "P", "HYP", "NN", "P", "DT"]
# # y_pred = ["NN", "VB", "P", "P", "DT", "P", "HYP"]
# # label = ["P","NN"]
# # for j in range (len(label)):
# #     tp = 0
# #     tn = 0
# #     fn = 0
# #     fp = 0
# #     if (len(y_true)) == (len(y_pred)):
# #         for i in range(len(y_true)):
# #             if (y_true[i] == label[j]) and (y_pred[i] == label[j]):
# #                 tp = tp+1
# #             elif (y_true[i] == label[j] ) and  (y_pred[i] != label[j]):
# #                 fn = fn+1
# #             elif (y_true[i] != label[j] ) and  (y_pred[i] == label[j]):
# #                 fp = fp+1
# #             elif (y_true[i] != label[j] ) and  (y_pred[i] != label[j]):
# #                 tn=tn+1
# #     print(tp,tn,fp,fn)
# #     print("sum of all",tp+tn+fp+fn)
# #     Precision = tp/(tp+fp)
# #     Recall = tp/(tp+fn)
# #     F1Score= 2*(Precision*Recall)/(Precision + Recall)
# #     print("Precision of Tag", label[j], ":",Precision)
# #     print("Recall of Tag", label[j], ":",Recall)
# #     print("F1Score of Tag", label[j], ":",F1Score)

































# ########## Temporary Data ##########
# true_tags = ["NN", "DT", "P", "HYP", "NN", "P", "DT","DT"] #correct(GoldStandard data)
# dummy_tags = ["NN", "VB", "P", "P", "DT", "P", "HYP","DT"]  #predicted(Dummy data)
# tag = ["NN","P","DT"] # Single label
# ########## Temporary Data ##########



# ########## Function to get tp,fp,fn,tn values ##########
# def matrix_values(y_true,y_pred,label): # check position of parameter
#     each_tag = {} 
#     for j in range (len(label)):
#         # initialize variables 
#         true_positive = 0
#         true_negative = 0
#         false_negative = 0
#         false_positive = 0
        
#         if (len(y_true)) == (len(y_pred)):          # procceed only if the length is the same
#             for i in range(len(y_true)):
#                 if (y_true[i] == label[j]) and (y_pred[i] == label[j]):
#                     true_positive = true_positive+1             # if conditions met then increment true_positive by 1
#                 elif (y_true[i] == label[j]) and (y_pred[i] != label[j]):
#                     false_negative = false_negative+1           # if conditions met then increment false_negative by 1
#                 elif (y_true[i] != label[j]) and (y_pred[i] == label[j]):
#                     false_positive = false_positive+1           # if conditions met then increment false_positive by 1
#                 elif (y_true[i] != label[j]) and (y_pred[i] != label[j]):
#                     true_negative=true_negative+1               # if conditions met then increment true_negative by 1
#         else:
#             print("******\nTHE LENGTH OF CORRECT and PREDICTED LIST IS DIFFERENT\n*****")
#         each_tag[label[j]] = [[true_positive, false_positive],[false_negative,true_negative]]
#         # print("True positive1",true_positive)
#         # print("False positive1",false_positive)
#         # print("False negative1",false_negative)
#         # print("True negative1",true_negative)
            
#     return each_tag
# ########## Function to get tp,fp,fn,tn values ##########



# # print(matrix_values(true_tags,dummy_tags,tag)) #testing function matrix_values



# ########## Function to calculate Precision & Recall ##########
# def calculate_precision_recall(y_true,y_pred,label):
#     values = matrix_values(y_true,y_pred,label)             # call matrix_values to get tp,fp,fn,tn values
#     PrecisionDict = {}
#     RecallDict = {}
#     Final_values = {"Precision":PrecisionDict, "Recall":RecallDict}
#     for i in values:
#     # Formula for Precision & Recall 
#         PrecisionDict[i] = values[i][[0][0]][0]/(values[i][[0][0]][0]+values[i][[0][0]][1])  #since i stored it in nested list/array this is how we get the values 
#         RecallDict[i] = values[i][[0][0]][0]/(values[i][[0][0]][0]+values[i][[1][0]][0])    
#     # # print("True negative",values[[1][0]][1]) 
#     return Final_values
# ########## Function to calculate Precision & Recall ##########



# # print(calculate_precision_recall(true_tags,dummy_tags,tag)) #testing function calculate_precision_recall



# ########## Function to calculate F1_Score ##########
# def calculate_f1score(y_true,y_pred,label):
#     prvalues = calculate_precision_recall(y_true,y_pred,label) # call matrix_values to get tp,fp,fn,tn values
#     # only_precision = values[i]
#     # Precision,Recall = calculate_precision_recall(y_true,y_pred,label) 
#     Precision = prvalues["Precision"]
#     Recall = prvalues["Recall"]
#     F1_ScoreDict = {}
#     for i in range(len(label)):  
#         # F1_Score= 2*(Precision.get(label[i])*Recall.get(label[i]))/(Precision.get(label[i]) + Recall.get(label[i]))
#         F1_ScoreDict[label[i]] = 2*(Precision.get(label[i])*Recall.get(label[i]))/(Precision.get(label[i]) + Recall.get(label[i]))
#     return F1_ScoreDict
# ########## Function to calculate F1_Score ##########



# # print(calculate_f1score(true_tags,dummy_tags,tag)) #testing function calculate_f1score



# ########## Function to calculate Macro F1_Score ##########
# def macro_average(y_true,y_pred,label):
#     FScores= calculate_f1score(y_true,y_pred,label)
#     total = 0
#     for i in FScores:
#         total = total + FScores[i]
#     macro_F1Score = total / len(FScores)
#     return macro_F1Score
# ########## Function to calculate Macro F1_Score ##########

# # print(macro_average(true_tags,dummy_tags,tag)) #testing function macro_average


####### Frequency for macro/micro F-score ############
# for i in devDict.keys():
#     print(i, ":", len(devDict[i]))

# print(len(devDict.keys()))




# ########## Function to calculate Micro F1_Score ##########
# def micro_average(y_true,y_pred,label):
#     f1score_values = calculate_f1score(y_true,y_pred,label)
#     counter = collections.Counter(y_true)
#     ckeys=counter.keys()
#     frequency = {}
#     frequencyXf1score = {}
#     for i in label:
#         for j in ckeys:
#             if i == j:
#                 frequency[i] = ((counter[j]*len(y_true))/100)
#                 frequencyXf1score[i] = (((counter[j]*len(y_true))/100)*f1score_values[i])
#     micro_value = 0
#     for i in frequencyXf1score:
#         micro_value = micro_value + frequencyXf1score[i]
#     return micro_value
    
# ########## Function to calculate Micro F1_Score ##########



# print(micro_average(true_tags,dummy_tags,tag)) #testing function macro_average

































# matrix of one hot encoded vecrors
# trains the model with that
# hidden markov model





























# import random

# def extract_features(word, prev_word=None, next_word=None):
#     features = {}
#     features['word'] = float(ord(word[0]))  # Using ASCII value of the first character as a numerical representation
#     features['prefix'] = float(ord(word[0]))  # Using ASCII value of the first character as a numerical representation
#     features['suffix'] = float(ord(word[-1]))  # Using ASCII value of the last character as a numerical representation
#     features['is_upper'] = float(word.isupper())  # Convert boolean to float
#     features['is_digit'] = float(word.isdigit())  # Convert boolean to float
#     features['has_hyphen'] = float('-' in word)  # Convert boolean to float
#     features['has_apostrophe'] = float("'" in word)  # Convert boolean to float
#     features['prev_word'] = float(ord(prev_word[0])) if prev_word else 0  # Using ASCII value of the first character as a numerical representation if prev_word is not None
#     features['next_word'] = float(ord(next_word[0])) if next_word else 0  # Using ASCII value of the first character as a numerical representation if next_word is not None
#     return features

# def read_data(file_path):
#     data = []
#     with open(file_path, 'r') as file:
#         sentence = []  # Initialize an empty list to store words and tags for each sentence
#         for line in file:
#             line = line.strip()  # Remove leading and trailing whitespace
#             if line:  # If the line is not empty
#                 parts = line.split('\t')  # Split the line by tab character
#                 word = parts[0]  # Extract the word
#                 pos_tag = parts[1]  # Extract the part-of-speech tag
#                 sentence.append((word, pos_tag))  # Append the word and tag to the current sentence
#             else:  # If the line is empty (end of sentence)
#                 if sentence:  # If the sentence is not empty
#                     # Extract features for each word in the sentence and append to data
#                     for i, (word, pos_tag) in enumerate(sentence):
#                         prev_word = sentence[i - 1][0] if i > 0 else None  # Get previous word
#                         next_word = sentence[i + 1][0] if i < len(sentence) - 1 else None  # Get next word
#                         features = extract_features(word, prev_word, next_word)  # Extract features for the word
#                         data.append((features, pos_tag))  # Append features and tag to data
#                     sentence = []  # Reset sentence for the next iteration
#     return data

# # Paths to the data files
# train_file = '/Users/mayurideshmukh/Desktop/Team-Lab/data/train.col'
# dev_file = '/Users/mayurideshmukh/Desktop/Team-Lab/data/dev.col'
# dev_predicted_file = '/Users/mayurideshmukh/Desktop/Team-Lab/data/dev-predicted.col'
# test_file = '/Users/mayurideshmukh/Desktop/Team-Lab/data/test.col'

# # Read data from the files
# train_data = read_data(train_file)
# dev_data = read_data(dev_file)
# dev_predicted_data = read_data(dev_predicted_file)
# test_data = read_data(test_file)

# # print(test_data)


# num_features = len(train_data[0][0])

# class Perceptron:
#     def __init__(self, num_features, class_labels):
#         # Initialize weights with random values between 0 and 1 for each class
#         self.weights = {class_label: [random.uniform(0, 1) for _ in range(num_features)] for class_label in class_labels}
#         # Initialize bias with a random value between 0 and 1 for each class
#         self.bias = {class_label: random.uniform(0, 1) for class_label in class_labels}

#     def predict(self, features):
#         scores = {}
#         for class_label in self.weights:
#             # Extract numerical values from the features dictionary
#             numerical_features = [features[key] for key in features]
#             # Calculate the weighted sum of features
#             weighted_sum = sum(feature * weight for feature, weight in zip(numerical_features, self.weights[class_label]))
#             # Add bias
#             weighted_sum += self.bias[class_label]
#             scores[class_label] = weighted_sum
#         # Return the class with the highest score
#         return max(scores, key=scores.get)

#     def update(self, features, label, learning_rate):
#         # Predict the label
#         prediction = self.predict(features)
#         # Update weights and bias based on prediction error
#         for class_label in self.weights:
#             if class_label == label:
#                 target = 1
#             else:
#                 target = 0
#             error = target - (1 if class_label == prediction else 0)
#             # Ensure features is a list to avoid TypeError
#             numerical_features = [features[key] for key in features]
#             self.weights[class_label] = [weight + learning_rate * error * feature for feature, weight in zip(numerical_features, self.weights[class_label])]
#             self.bias[class_label] += learning_rate * error

# # Get all unique class labels from the training data
# class_labels = set(label for _, label in train_data)

# # Initialize Perceptron with the number of features and class labels
# perceptron = Perceptron(num_features, class_labels)


# # print(class_labels)
# # print(perceptron)
# for features, label in train_data:
#         prediction = perceptron.predict(features)
#         if prediction == label:
#             print(f"Prediction: {prediction}, Label: {label}")




































# def contains_digit(s):
#     isdigit = str.isdigit
#     return any(map(isdigit,s))

# print(contains_digit("20th"))











































import operator
train_file = "/Users/mayurideshmukh/Desktop/Team-Lab/data/dev-predicted.col"
gold_standard_file = "/Users/mayurideshmukh/Desktop/Team-Lab/data/dev.col"
L_train_file = "/Users/mayurideshmukh/Desktop/Team-Lab/data/train.col"

def create_corpus_C(training_file):
    sentences = []
    current_sentence = []

    with open(training_file, 'r') as file:
        with open(r'/Users/mayurideshmukh/Desktop/Team-Lab/data/corpus_without_tags.txt', 'w') as fp:
            for line in file:
                if line.strip():  # Non-empty line
                    word, tag = line.split()
                    current_sentence.append((word))
                    fp.write("%s\n" % word)
                else:  # Empty line indicates end of sentence
                    if current_sentence:
                        sentences.append(current_sentence)
                        fp.write("%s\n" % "")
                        current_sentence = []
    
    # Append the last sentence if it's not empty and doesn't end with an empty line
    if current_sentence:
        sentences.append(current_sentence)
    
    return sentences

# f = open('/Users/mayurideshmukh/Desktop/Team-Lab/data/filename.txt', 'w')
# print(parse_training_data(train_file), file = f)
# for i in parse_training_data(train_file):
    # # print(i)
    # for j in i:
        # # print(parse_training_data(j), file = f)
        # print(j)


# print(create_corpus_C(train_file))

transformation_list_T = []

# names = ['Jessa', 'Eric', 'Bob']

# # open file in write mode
# with open(r'/Users/mayurideshmukh/Desktop/Team-Lab/data/filename.txt', 'w') as fp:
#     for item in names:
#         # write each item on a new line
#         fp.write("%s\n" % item)
#     print('Done')











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


def calculate_possible_tags(word_to_tag):
    word_to_majority_tag = {}
    all_posible_tags = {}
    # with open(r'/Users/mayurideshmukh/Desktop/Team-Lab/data/possible_tags.txt', 'w') as fp:
    for word, tag_counts in word_to_tag.items():
        all_posible_tags[word] = tag_counts
        # print(word, ":",tag_counts)
        majority_tag = max(tag_counts, key=tag_counts.get)
        word_to_majority_tag[word] = majority_tag
        # fp.write("%s\n" % all_posible_tags)
    # print(all_posible_tags)
    new_dict = {}
    with open(r'/Users/mayurideshmukh/Desktop/Team-Lab/data/possible_tags.txt', 'w') as fp:
        for i in all_posible_tags:
            # print(i , ":", all_posible_tags[i])
            # print(all_posible_tags[i])
            sorted_d = dict( sorted(all_posible_tags[i].items(), key=operator.itemgetter(1), reverse=True))
            # print(sorted_d)
            new_dict[i] = sorted_d
            fp.write("%s\n" % {i : sorted_d})
    return new_dict



#logic
L='/Users/mayurideshmukh/Desktop/Team-Lab/data/possible_tags.txt'
C='/Users/mayurideshmukh/Desktop/Team-Lab/data/corpus_without_tags.txt'



def read_and_map_files(file1_path, file2_path,output_path):
    # Dictionary to store mappings from file 1
    word_to_tag = {}

    # Read and parse file 1
    with open(file1_path, 'r') as file1:
        for line in file1:
            # Evaluate the string to convert it into a dictionary
            entry = eval(line.strip())
            # Extract the word and its associated tag dictionary
            word = list(entry.keys())[0]
            tag_dict = entry[word]
            # Get the first tag (assuming the tags are sorted by frequency in file 1)
            first_tag = list(tag_dict.keys())[0]
            # Map the word to its first tag
            word_to_tag[word] = first_tag

    # Read file 2 and perform mapping
    mapped_words = []
    with open(file2_path, 'r') as file2:
        for line in file2:
            word = line.strip()
            if word in word_to_tag:
                # Map the word to its corresponding tag from file 1
                mapped_words.append((word, word_to_tag[word]))
            else:
                if word == '':
                    mapped_words.append(('', ''))
                else:

                # If the word is not found in file 1, use a default tag or handle accordingly
                # Here, we'll use 'UNK' (unknown) as a placeholder
                    mapped_words.append((word, 'UNK'))

    with open(output_path, 'w') as output_file:
        for word, tag in mapped_words:
            output_file.write(f"{word}   {tag}\n")


    return mapped_words

# Example usage:
file1_path = 'file1.txt'
file2_path = 'file2.txt'

mapped_words = read_and_map_files(L, C, "/Users/mayurideshmukh/Desktop/Team-Lab/data/annotated_corpus.txt")

# # Display the mapped words and their tags
# for word, tag in mapped_words:
#     print(f"{word}: {tag}")
# print("hello")

# mapped_words = map_words_to_tags(L, C, "/Users/mayurideshmukh/Desktop/Team-Lab/data/annotated_corpus.txt")

# # Display the mapped words and their tags
# for word, tag in mapped_words:
#     print(f"{word}: {tag}")


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


annotated_parsed = parse_training_data('/Users/mayurideshmukh/Desktop/Team-Lab/data/annotated_corpus.txt')
gold_standard_parsed=parse_training_data(gold_standard_file)

errors = detect_errors(annotated_parsed, gold_standard_parsed)

error_word = []
# Print detected errors
for error in errors:
    print(f"Error: Predicted tag '{error[1]}' for word '{error[0]}' is incorrect; gold standard tag is '{error[2]}'")
    error_word.append(error[0])
#     if error[0] == '-':
#         print (error[0], error[1], error[2])

    
    
# print(gold_standard_parsed)
from collections import Counter
# list1=['apple','egg','apple','banana','egg','apple']
counts = Counter(error_word)
# print(counts)
print(len(errors))
# print(number)


















def learning_algorithm():
    # logic
    return