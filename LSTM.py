import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import f1_score
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Embedding, Dense
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import sys

language = sys.argv[1]

print("Loading dataset...")
if not language == "en":
    data = pd.read_csv("train{}.csv".format(language))
    test = pd.read_csv("test{}.csv".format(language))
else:
    data = pd.read_csv("train{}.col".format(language), delimiter='\t', header=None, names=['Word', 'Tag'])
    test = pd.read_csv("test{}.col".format(language), delimiter='\t', header=None, names=['Word', 'Tag'])
print("Done!")

# Removing any NaNs
data = data.dropna(subset=['Word', 'Tag'])
data['Word'] = data['Word'].astype(str)


words = data['Word'].tolist()
tags = data['Tag'].tolist()

# Convert tags to numerical labels
tag_encoder = LabelEncoder()
y_encoded = tag_encoder.fit_transform(tags)

# Tokenize words and convert to sequences of integers
tokenizer = Tokenizer()
tokenizer.fit_on_texts(words)
sequences_X = tokenizer.texts_to_sequences(words)

# Pad sequences to ensure uniform length
X_padded = pad_sequences(sequences_X, padding='post')

# Define LSTM model
model = Sequential()
model.add(Embedding(input_dim=len(tokenizer.word_index) + 1, output_dim=64, input_length=X_padded.shape[1]))  
model.add(LSTM(units=64, return_sequences=False))  
model.add(Dense(units=len(tag_encoder.classes_), activation='softmax'))  

# Compile the model
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Train the model on the entire dataset
history = model.fit(X_padded, y_encoded, epochs=10, batch_size=32, validation_split=0.1)

# Plot training history
import matplotlib.pyplot as plt

plt.plot(history.history['loss'], label='Loss')
plt.plot(history.history['accuracy'], label='Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Value')
plt.title('Training Loss and Accuracy')
plt.legend()
plt.show()

# Predict on the train set
y_pred_prob = model.predict(X_padded)
y_pred = np.argmax(y_pred_prob, axis=1)

# Calculate F1 score on the train set
f1_train_weighted = f1_score(y_encoded, y_pred, average='weighted')
f1_train_macro = f1_score(y_encoded, y_pred, average='macro')
f1_train_micro = f1_score(y_encoded, y_pred, average='micro')
print(f'Weighted F1 Score on Train Data: {f1_train_weighted}')
print(f'Macro F1 Score on Train Data: {f1_train_macro}')
print(f'Micro F1 Score on Train Data: {f1_train_micro}')




test = test.dropna(subset=['Word', 'Tag'])
test['Word'] = test['Word'].astype(str)

test_words = test['Word'].tolist()
test_tags = test['Tag'].tolist()

# Convert test tags to numerical labels using the same encoder fitted on training data
y_test_encoded = tag_encoder.transform(test_tags)

# Tokenize and pad sequences for test data
test_sequences_X = tokenizer.texts_to_sequences(test_words)
X_test_padded = pad_sequences(test_sequences_X, padding='post', maxlen=X_padded.shape[1])  # same length as training data

# Evaluation
loss, accuracy = model.evaluate(X_test_padded, y_test_encoded)
print(f'Test Accuracy: {accuracy}')

# Prediction on the test set
y_pred_prob = model.predict(X_test_padded)
y_pred = np.argmax(y_pred_prob, axis=1)

f1_test_weighted = f1_score(y_test_encoded, y_pred, average='weighted')
f1_test_macro = f1_score(y_test_encoded, y_pred, average='macro')
f1_test_micro = f1_score(y_test_encoded, y_pred, average='micro')
print(f'Weighted F1 Score on Test Data: {f1_test_weighted}')
print(f'Macro F1 Score on Test Data: {f1_test_macro}')
print(f'Micro F1 Score on Test Data: {f1_test_micro}')
