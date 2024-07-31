from sklearn.feature_extraction import DictVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, precision_score, recall_score, classification_report
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

language = sys.argv[1]

# Create context window function for the Logistic regression to consider context as suggested
def create_context_windows(words, window_size=5):
    context_words = []
    for i in range(len(words)):
        window = words[max(i - window_size, 0):i] + \
                 [words[i]] + \
                 words[i + 1:i + 1 + window_size]
        window = ['<PAD>'] * (2 * window_size + 1 - len(window)) + window
        context_words.append(window)
    return context_words

print("Loading dataset...")
if not language == "en":
    data = pd.read_csv("data/processed/train{}.csv".format(language))
    test_data = pd.read_csv("data/processed/test{}.csv".format(language))
else:
    data = pd.read_csv("data/processed/train{}.col".format(language), delimiter='\t', header=None, names=['Word', 'Tag'])
    test_data = pd.read_csv("data/processed/test{}.col".format(language), delimiter='\t', header=None, names=['Word', 'Tag'])
print("Done!")


words = data['Word'].tolist()
tags = data['Tag'].tolist()

print("Preparing Label Encoder...")
tag_encoder = LabelEncoder()
y_encoded = tag_encoder.fit_transform(tags)
print("Done!")

# Creation of the context windows
context_words = create_context_windows(words, window_size=5)


X = [{'w-2': context[0], 'w-1': context[1], 'w': context[2], 'w+1': context[3], 'w+2': context[4]} for context in context_words]

print("Preparing Vectorizer...")
vectorizer = DictVectorizer(sparse=True)
X_train = vectorizer.fit_transform(X)
print("Done!")

print("Imputing Missing Values...")
imputer = SimpleImputer(strategy='mean')
X_train_imputed = imputer.fit_transform(X_train)
print("Done!")

print("Training the model...")
# Training the model 
model = LogisticRegression(max_iter=1000, solver='lbfgs', multi_class='multinomial')
model.fit(X_train_imputed, y_encoded)
print("Done!")

print("Making Predictions...")
# Prediction on the training set to calculate metrics
y_train_pred_encoded = model.predict(X_train_imputed)
y_train_pred = tag_encoder.inverse_transform(y_train_pred_encoded)
print("Done!")

print("Evaluating the predictions...")
# Evaluation
precision_train = precision_score(tags, y_train_pred, average='weighted')
recall_train = recall_score(tags, y_train_pred, average='weighted')
f1_train = f1_score(tags, y_train_pred, average='weighted')
print(f"Precision on Training Data: {precision_train}")
print(f"Recall on Training Data: {recall_train}")
print(f"F1 Score on Training Data: {f1_train}")

# Print detailed classification report
print("Classification Report on Training Data:")
print(classification_report(tags, y_train_pred))





test_words = test_data['Word'].tolist()
test_tags = test_data['Tag'].tolist()

# Convert test tags to numerical labels using the same encoder fitted on training data
y_test_encoded = tag_encoder.transform(test_tags)

# Create context windows for the test data
context_test_words = create_context_windows(test_words, window_size=5)

# Convert words to feature dictionaries with context for the test data
X_test = [{'w-2': context[0], 'w-1': context[1], 'w': context[2], 'w+1': context[3], 'w+2': context[4]} for context in context_test_words]

# Convert feature dictionaries to sparse numeric representation
X_test_transformed = vectorizer.transform(X_test)

# Impute missing values (replace NaN with mean of each feature)
X_test_imputed = imputer.transform(X_test_transformed)

# Predict on the test set
y_test_pred_encoded = model.predict(X_test_imputed)
y_test_pred = tag_encoder.inverse_transform(y_test_pred_encoded)

# Calculate and print precision, recall, and F1 score on the test data
precision_test = precision_score(test_tags, y_test_pred, average='weighted')
recall_test = recall_score(test_tags, y_test_pred, average='weighted')
f1_test = f1_score(test_tags, y_test_pred, average='weighted')
print(f"Precision on Test Data: {precision_test}")
print(f"Recall on Test Data: {recall_test}")
print(f"F1 Score on Test Data: {f1_test}")

# Print detailed classification report for test data
print("Classification Report on Test Data:")
print(classification_report(test_tags, y_test_pred))

# Plotting loss and accuracy 
# Here, we will use training and test accuracy to plot
train_accuracy = model.score(X_train_imputed, y_encoded)
test_accuracy = model.score(X_test_imputed, y_test_encoded)

# Simulation 
epochs = np.arange(1, 2)  # LR does not have epochs, so we simulate a single step

# Plotting the results
plt.figure(figsize=(10, 5))

# Plot accuracy
plt.plot(epochs, [train_accuracy] * len(epochs), label='Training Accuracy', marker='o')
plt.plot(epochs, [test_accuracy] * len(epochs), label='Test Accuracy', marker='x')

plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.title('Training and Test Accuracy')
plt.legend()
plt.show()
