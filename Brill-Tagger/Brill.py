import operator
import sys
import os
import evaluation  # type: ignore

def contains_digit(s):
    isdigit = str.isdigit 
    return any(map(isdigit,s))


train_file = os.path.join(sys.path[0], "test.col")
gold_standard_file = os.path.join(sys.path[0], "test.col")
L_train_file = os.path.join(sys.path[0], "train.col")


#### Create a corpus without tags ####

def create_corpus_C(training_file):
    sentences = []
    current_sentence = []

    with open(training_file, 'r') as file:
        with open(os.path.join(sys.path[0], "corpus_without_tags.txt"), 'w') as fp:
            for line in file:
                if line.strip():  # Non-empty line
                    word, tag = line.split()
                    current_sentence.append((word)) #app the w into s
                    fp.write("%s\n" % word)
                else:  # Empty line indicates end of sentence
                    if current_sentence:
                        #update sentences so sentences is [[..],[..],[..]...]
                        sentences.append(current_sentence)
                        fp.write("%s\n" % "")
                        current_sentence = []
    
    # Append the last sentence if it's not empty and doesn't end with an empty line
    if current_sentence:
        sentences.append(current_sentence)
    
    return sentences


create_corpus_C(train_file)

#### Create a corpus without tags ####





#### parse corpus sentence wise ####

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

#### parse corpus sentence wise ####




#### convert corpus sentence to a word : tag Dictionary ####
# the : DT 7, NN 2
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

#### convert corpus sentence to a word : tag Dictionary ####



#### calculate possible tags for each word { word : {tagA : no. , tagB : no. ...} ####
#### using train.col for this because it has a lot of data ####


# the : DT :7 : NN 17
def calculate_possible_tags(word_to_tag):
    word_to_majority_tag = {}
    all_posible_tags = {}
    # with open(r'/Users/mayurideshmukh/Desktop/Team-Lab/data/possible_tags.txt', 'w') as fp:
    for word, tag_counts in word_to_tag.items():
        all_posible_tags[word] = tag_counts
        # print(word, ":",tag_counts)
        majority_tag = max(tag_counts, key=tag_counts.get)
        word_to_majority_tag[word] = majority_tag
    new_dict = {}
    with open(os.path.join(sys.path[0], "possible_tags.txt"), 'w') as fp:
        for i in all_posible_tags:
            sorted_d = dict( sorted(all_posible_tags[i].items(), key=operator.itemgetter(1), reverse=True))
            new_dict[i] = sorted_d
            fp.write("%s\n" % {i : sorted_d})
    return new_dict


#### calculate possible tags for each word { word : {tagA : no. , tagB : no. ...} ####


predicted_parsed = parse_training_data(train_file)
gold_standard_parsed=parse_training_data(gold_standard_file)
word_to_tag = build_word_to_tag_dict(predicted_parsed)
word_to_possible_tags = calculate_possible_tags(word_to_tag)


All_possible_tags=os.path.join(sys.path[0], "possible_tags.txt")
Corpus_without_tags=os.path.join(sys.path[0], "corpus_without_tags.txt")


#### annotate the corpus with majority tag ####

def read_and_map_files(file1_path, file2_path,output_path):
    # Dictionary to store mappings from file 1
    word_to_tag = {}

    # Read and parse file 1
    with open(file1_path, 'r') as file1:
        for line in file1:
            entry = eval(line.strip())
            word = list(entry.keys())[0] # take only the words
            tag_dict = entry[word]  # take all the values
            first_tag = list(tag_dict.keys())[0]  # take only the 1st value
            
            word_to_tag[word] = first_tag # the : DT

    # Read file 2 and perform mapping
    mapped_words = []
    with open(file2_path, 'r') as file2:
        for line in file2:
            word = line.strip()
            if word in word_to_tag:
                mapped_words.append((word, word_to_tag[word])) # Map the word to its corresponding tag from file 1
            elif word == '':
                    mapped_words.append(('', ''))
            else:
                # use 'UNK' (unknown) as a placeholder If the word is not found in file 
                mapped_words.append((word, 'UNK'))

    with open(output_path, 'w') as output_file:
        for word, tag in mapped_words:
            output_file.write(f"{word}   {tag}\n")


    return mapped_words


Annotated_corpus_majority_tags = os.path.join(sys.path[0], "annotated_corpus.txt")
mapped_words = read_and_map_files(All_possible_tags, Corpus_without_tags, Annotated_corpus_majority_tags)


#### annotate the corpus with majority tag ####






#### apply rules ####

def apply_transformational_rules(sentences,output_file):
    transformed_sentences = []
    with open(output_file, 'w') as f:
        for sentence in sentences:
            transformed_sentence = []
            previous_tag = None #previous tags,for 1st there´s
            
            for i, (word, tag) in enumerate(sentence):
                # Apply transformational rules based on context
                if word == 'continued' and i < len(sentence) - 1 and (sentence[i + 1][1] == 'NN' or sentence[i + 1][1] == 'VBG' ):
                    transformed_sentence.append(('continued', 'VBN'))  # 'all' before a DT is likely a predeterminer 
                elif word.isalpha() and (len(word) == 1 and sentence[i + 1][1] == ':'):
                    transformed_sentence.append((word, 'LS'))   
                elif  word == '-':
                    if previous_tag == 'LS':
                        transformed_sentence.append(('-', ':'))   
                    else:
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
                elif tag == 'NN':
                    # Rule: NN --> VBP if the preceding tag is 'PRP'
                    if previous_tag == 'PRP':
                        transformed_sentence.append((word, 'VBP'))
                    # Rule: NN --> JJ if the following tag is 'JJ'
                    elif i + 1 < len(sentence) and sentence[i + 1][1] == 'JJ':
                        transformed_sentence.append((word, 'JJ'))
                    # Rule: NN --> IN if the preceding tag is '.'
                    elif previous_tag == '.':
                        transformed_sentence.append((word, 'IN'))
                    else:
                        transformed_sentence.append((word, tag))  # Keep original tag if no rule applies
                elif tag == 'NNP':
                    # Rule: NNP --> NN if the tag of words i-3...i-1 is JJ
                    if i >= 3 and all(sentence[i - j][1] == 'JJ' for j in range(1, 4)):
                        transformed_sentence.append((word, 'NN'))
                    # Rule: NNP --> NNP if the tag of words i+1...i+2 is NNP
                    elif i + 2 < len(sentence) and all(sentence[i + j][1] == 'NNP' for j in range(1, 3)):
                        transformed_sentence.append((word, 'NNP'))
                    else:
                        transformed_sentence.append((word, tag))  # Keep original tag if no rule applies
                elif word == 'to':
                    # Determine tag for 'to' based on previous tag
                    ptags = ['VB', 'VBP', 'MD',  'NN', 'JJ', 'NNS', 'RB', 'VBZ', 'VBD']
                    if previous_tag in ptags and (sentence[i + 1][1] == 'VB' or sentence[i + 1][1] == 'VBZ' or sentence[i + 1][1] == 'VBD'  ):
                        transformed_sentence.append(('to', 'TO'))  # Tag 'to' as infinitive marker preposition if next tag is verb
                    elif previous_tag in ptags and (sentence[i + 1][1] == 'DT' or sentence[i +1][1] ==  'NN') and sentence[i +2][1] not in ['VB', 'VBZ', 'VBD']:
                        transformed_sentence.append(('to', 'IN'))  # Tag 'to' as infinitive marker preposition if next tag is verb
                    else:
                        transformed_sentence.append(('to', 'IN'))  # Otherwise, tag 'to' as ipreposition
                elif word == 'all' and i < len(sentence) - 1 and (sentence[i + 1][1] == 'DT' or sentence[i + 1][1] == 'PRP$' ):
                    transformed_sentence.append(('all', 'PDT'))  # 'all' before a DT is likely a predeterminer
                elif word == 'about' and i > 0 and sentence[i - 1][1] == 'IN':
                    transformed_sentence.append(('about', 'IN'))  # Tag 'about' as IN when it introduces a prepositional phrase
                elif word in ['he', 'HE','He', 'she', 'SHE','She', 'it', 'IT']:
                    transformed_sentence.append((word, 'PRP'))  # Tag 'he' as PRP (subject pronoun)
                elif word.isdigit() or contains_digit(word):
                    # number.append(word) #1400s : CD, one : CD 1:CD mid-1970s : JJ
                    transformed_sentence.append((word, 'CD'))  # Tag all digits as cardinal numbers
                else:
                    transformed_sentence.append((word, tag))  # Keep original tag if no rule applies
                
                # Update previous tag for next iteration
                previous_tag = tag
            
            
            for word, tag in transformed_sentence:
                f.write(f"{word}\t{tag}")
                f.write("\n")  # Write a blank line to separate sentences
            transformed_sentences.append(transformed_sentence)

    return transformed_sentences

#### apply rules ####

Annotated_parsed=parse_training_data(Annotated_corpus_majority_tags)
after_rule_corpus = os.path.join(sys.path[0], "after_rule_corpus.txt")
transformed_predicted_tags = apply_transformational_rules(Annotated_parsed,after_rule_corpus)


#### tag 1 sentnece after applying rules ####

def brill_tagger(sentence, word_to_majority_tag):
    tagged_sentence = []
    words = []
    current_token = ""
    for char in sentence:
        if char in [" ", ",", "."]:
            if current_token:
                words.append(current_token)
                current_token = ""  # Reset current_token
            if char != ' ':
                words.append(char)
        else:
            current_token += char
    if current_token:
        words.append(current_token)

    for word in words:
        if word in word_to_majority_tag:
            # print(word_to_majority_tag[word])
            for i in word_to_majority_tag[word]:
                # print(i)
                tagged_sentence.append((word, i))
        else:
            # If word is not in training data, default to a common tag like 'NN' (noun)
            tagged_sentence.append((word, 'NN'))
    
    return tagged_sentence

#### tag 1 sentnece after applying rules ####


#### Testing on 1 sentence ####

final_file = after_rule_corpus
final_parsed=parse_training_data(final_file)
word_to_tag = build_word_to_tag_dict(final_parsed)
word_to_tag_GS = build_word_to_tag_dict(gold_standard_parsed)

sample_sentence = "The economy's temperature will be taken from several vantage points this week, with readings on trade ,output, housing and inflation ."

brill_tags = brill_tagger(sample_sentence, word_to_tag)
brill_tags_GC = brill_tagger(sample_sentence, word_to_tag_GS)

#### Testing on 1 sentence ####






#### evaluate ####

final_annotated_tags = []
for i in final_parsed:
    for j in i:
        final_annotated_tags.append(j[1])


final_gold_tags = []
for i in gold_standard_parsed:
    for j in i:
        final_gold_tags.append(j[1])


labels = ["NN","DT","PRP","POS"]
print("Macro Average values for given labels : ",evaluation.macro_average(final_gold_tags,final_annotated_tags,labels)) #testing function macro_average
# print("Micro Average values for given labels : ",evaluation.micro_average(final_gold_tags,final_annotated_tags,labels)) #testing function micro_average
print("F1 Score for given labels : ",evaluation.calculate_f1score(final_gold_tags,final_annotated_tags,labels)) #testing function calculate_f1score
print("Precision-Recall for given labels : ",evaluation.calculate_precision_recall(final_gold_tags,final_annotated_tags,labels)) #testing function calculate_f1score
print("Matrix values for given labels : ",evaluation.matrix_values(final_gold_tags,final_annotated_tags,labels)) #testing function calculate_f1score

#### evaluate ####






