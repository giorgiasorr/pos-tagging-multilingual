import random
from FeatureExtraction import extract_features

def read_data(file_path):
    data = []
    with open(file_path, 'r') as file:
        sentence = []  # Initialize an empty list to store words and tags for each sentence
        for line in file:
            line = line.strip()  # Remove leading and trailing whitespace
            if line:  # If the line is not empty
                parts = line.split('\t')  # Split the line by tab character
                word = parts[0]  # Extract the word
                pos_tag = parts[1]  # Extract the part-of-speech tag
                sentence.append((word, pos_tag))  # Append the word and tag to the current sentence
            else:  # If the line is empty (end of sentence)
                if sentence:  # If the sentence is not empty
                    # Extract features for each word in the sentence and append to data
                    for i, (word, pos_tag) in enumerate(sentence):
                        prev_word = sentence[i - 1][0] if i > 0 else None  # Get previous word
                        next_word = sentence[i + 1][0] if i < len(sentence) - 1 else None  # Get next word
                        features = extract_features(word, prev_word, next_word)  # Extract features for the word
                        data.append((features, pos_tag))  # Append features and tag to data
                    sentence = []  # Reset sentence for the next iteration
    return data

# Paths to the data files
train_file = 'train.col'
dev_file = 'dev.col'
dev_predicted_file = 'dev-predicted.col'
test_file = 'test.col'

# Read data from the files
train_data = read_data(train_file)
dev_data = read_data(dev_file)
dev_predicted_data = read_data(dev_predicted_file)
test_data = read_data(test_file)

# Calculate the number of features based on the first training example
num_features = len(train_data[0][0])

class Perceptron:
    def __init__(self, num_features, class_labels):
        # Initialize weights with random values between 0 and 1 for each class
        self.weights = {class_label: [random.uniform(0, 1) for _ in range(num_features)] for class_label in class_labels}
        # Initialize bias with a random value between 0 and 1 for each class
        self.bias = {class_label: random.uniform(0, 1) for class_label in class_labels}

    def predict(self, features):
        scores = {}
        for class_label in self.weights:
            # Extract numerical values from the features dictionary
            numerical_features = [features[key] for key in features]
            # Calculate the weighted sum of features
            weighted_sum = sum(feature * weight for feature, weight in zip(numerical_features, self.weights[class_label]))
            # Add bias
            weighted_sum += self.bias[class_label]
            scores[class_label] = weighted_sum
        # Return the class with the highest score
        return max(scores, key=scores.get)

    def update(self, features, label, learning_rate):
        # Predict the label
        prediction = self.predict(features)
        # Update weights and bias based on prediction error
        for class_label in self.weights:
            if class_label == label:
                target = 1
            else:
                target = 0
            error = target - (1 if class_label == prediction else 0)
            # Ensure features is a list to avoid TypeError
            numerical_features = [features[key] for key in features]
            self.weights[class_label] = [weight + learning_rate * error * feature for feature, weight in zip(numerical_features, self.weights[class_label])]
            self.bias[class_label] += learning_rate * error

# Get all unique class labels from the training data
class_labels = set(label for _, label in train_data)

# Initialize Perceptron with the number of features and class labels
perceptron = Perceptron(num_features, class_labels)

"""
# Train the Perceptron
learning_rate = 0.1
num_epochs = 10

for epoch in range(num_epochs):
    #print(f"Epoch {epoch + 1}:")
    total_loss = 0  # Initialize total loss for the epoch
    for features, label in train_data:
        prediction = perceptron.predict(features)
        #print(f"Prediction: {prediction}, Label: {label}")
        loss = int(prediction != label)  # Calculate loss (1 if prediction is incorrect, 0 otherwise)
        total_loss += loss  # Accumulate total loss for the epoch
        perceptron.update(features, label, learning_rate)
    # Calculate and print average loss for the epoch
    average_loss = total_loss / len(train_data)
    #print(f"Average Loss: {average_loss:.4f}")
"""