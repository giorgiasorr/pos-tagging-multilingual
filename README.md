# Evaluating the Brill Tagger Against Modern POS Tagging Techniques: A Comparative Study of Rule-Based, HMM, LSTM, and Logistic Regression Models

This project presents a comparative study of classical and modern approaches to Part-of-Speech (POS) tagging across English, Italian, and French.

It evaluates whether the Brill tagger, one of the earliest transformation-based models, remains competitive against modern machine learning and deep learning approaches such as HMM, Logistic Regression, and LSTM.

The study focuses on performance, robustness across languages, and the trade-off between rule-based and data-driven methods.

A detailed academic report is included in the `report/` directory.


## Project Objectives

- Implement multiple POS tagging approaches from scratch
- Compare rule-based, probabilistic, and neural models
- Evaluate performance across English, Italian, and French
- Assess whether the Brill tagger remains competitive with modern methods
- Analyze error patterns and model limitations


## Key Features

- End-to-end POS tagging pipeline for multiple languages
- Implementation of classical and modern NLP models:
  - Rule-Based Tagger
  - Brill Transformation-Based Tagger
  - Hidden Markov Model (HMM)
  - Logistic Regression
  - LSTM Neural Network
- Multilingual evaluation framework
- Standardized performance metrics:
  - Accuracy
  - Macro F1-score
  - Micro F1-score
- Comparative analysis across models and languages


## Methods & Techniques

### Rule-Based Tagging
A deterministic tagging system based on handcrafted linguistic rules and unigram frequency statistics. Contextual rules are applied to refine initial tag assignments.

### Brill Tagger
A transformation-based learning model that:
- Starts with unigram tagging
- Learns correction rules from errors
- Iteratively improves tagging accuracy based on context patterns

### Hidden Markov Model (HMM)
A probabilistic sequence model using:
- Transition probabilities between tags
- Emission probabilities for word-tag relations
- Viterbi algorithm for optimal sequence decoding

### Logistic Regression
A discriminative model using:
- Context window (target word ±2 neighbors)
- Feature vectors via DictVectorizer
- Probability-based tag prediction

### LSTM (Long Short-Term Memory)
A deep learning sequence model using:
- Word embeddings (64-dimensional)
- LSTM layer (64 units)
- Softmax output for tag classification
- Sequential context modeling


## Experiments

### Datasets

- English: IMS Server dataset
  - 2,937 training sentences
  - 1,337 test sentences
  - 48 POS tags

- Italian and French: Universal Dependencies (UD)
  - Italian: 9,940 training, 355 test (18 tags)
  - French: 1,684 training, 344 test (17 tags)

### Experimental Setup

Each model was evaluated independently per language using:

- Accuracy
- Macro averaged F1-score
- Micro averaged F1-score

### Reproducibility

Run each model from the project root directory:

```bash
python RuleBased.py
python Brill.py
python hmm_en.py
python hmm_it.py
python hmm_fr.py
python Logistic_Regression.py en
python Logistic_Regression.py it
python Logistic_Regression.py fr
python LSTM.py en
python LSTM.py it
python LSTM.py fr
```


## Results

### English Performance

| Model | Accuracy | Macro F1 | Micro F1 |
|------|----------|----------|----------|
| Rule-Based | 0.9049 | 0.8164 | 0.9050 |
| Brill | 0.9180 | 0.8496 | 0.9181 |
| HMM | 0.8978 | 0.7503 | 0.8978 |
| Logistic Regression | 0.9543 | 0.8792 | 0.9463 |
| LSTM | 0.7875 | 0.6329 | 0.8032 |

### Italian Performance

| Model | Accuracy | Macro F1 | Micro F1 |
|------|----------|----------|----------|
| Brill | 0.9161 | 0.8414 | 0.9161 |
| HMM | 0.8438 | 0.6775 | 0.8438 |
| Logistic Regression | 0.8329 | 0.2704 | 0.4848 |
| LSTM | 0.8943 | 0.7885 | 0.8959 |


### French Performance

| Model | Accuracy | Macro F1 | Micro F1 |
|------|----------|----------|----------|
| Brill | 0.8977 | 0.8346 | 0.8978 |
| HMM | 0.8700 | 0.7501 | 0.8700 |
| Logistic Regression | 0.5300 | 0.7200 | 0.5200 |
| LSTM | 0.8746 | 0.7832 | 0.8745 |


## Key Findings

- Brill Tagger is consistently strong across languages
- Logistic Regression performs best on English but does not generalize well
- LSTM improves sequence modeling but struggles with rare words and long dependencies
- HMM provides stable but lower overall performance
- Rule-based system remains competitive despite simplicity


## Error Analysis

### LSTM
LSTM struggles with:
- Long-range dependencies
- Rare words
- Multiword expressions

### Logistic Regression
The limitations are:
- Weak handling of ambiguity
- Poor performance on low-frequency tags in Italian and French
- Limited contextual understanding even with a windowed feature set


## Project Structure

```text
pos-tagging-project/
│
├── RuleBased.py
├── Brill.py
├── hmm_en.py
├── hmm_it.py
├── hmm_fr.py
├── Logistic_Regression.py
├── LSTM.py
├── evaluation.py
│
├── train.col
├── test.col
├── it_train.col
├── it_test.col
├── fr_train.col
├── fr_test.col
│
├── report/
│   └── POS_tagging_comparative_study.pdf
│
└── README.md
```


## Limitations

- Rule-Based system only implemented for English
- LSTM trained with relatively small architecture and limited epochs
- Logistic Regression depends heavily on feature engineering
- Uneven dataset sizes across languages


## Future Work

- Extend evaluation to more languages, especially low-resource languages
- Explore BiLSTM and transformer-based models
- Improve feature engineering for statistical models
- Combine rule-based and neural hybrid approaches
- Apply contextual embeddings such as BERT for tagging
- Improve Brill tagger with richer contextual patterns
