import random

def extract_features(word, prev_word=None, next_word=None):
    features = {}
    features['word'] = float(ord(word[0]))  # Using ASCII value of the first character as a numerical representation
    features['prefix'] = float(ord(word[0]))  # Using ASCII value of the first character as a numerical representation
    features['suffix'] = float(ord(word[-1]))  # Using ASCII value of the last character as a numerical representation
    features['is_upper'] = float(word.isupper())  # Convert boolean to float
    features['is_digit'] = float(word.isdigit())  # Convert boolean to float
    features['has_hyphen'] = float('-' in word)  # Convert boolean to float
    features['has_apostrophe'] = float("'" in word)  # Convert boolean to float
    features['prev_word'] = float(ord(prev_word[0])) if prev_word else 0  # Using ASCII value of the first character as a numerical representation if prev_word is not None
    features['next_word'] = float(ord(next_word[0])) if next_word else 0  # Using ASCII value of the first character as a numerical representation if next_word is not None
    return features

# Dummy training data (features, label)
training_data = [
    (extract_features('The'), 0),  # Example: The -> 0 (not a verb)
    (extract_features('quick'), 1), # Example: quick -> 1 (is a verb)
    # Add more examples as needed
]

# Calculate the number of features based on the first training example
num_features = len(training_data[0][0])

class Perceptron:
    def __init__(self, num_features):
        # Initialize weights with random values between 0 and 1
        self.weights = [random.uniform(0, 1) for _ in range(num_features)]
        # Initialize bias with a random value between 0 and 1
        self.bias = random.uniform(0, 1)

    def predict(self, features):
        # Extract numerical values from the features dictionary
        numerical_features = [features[key] for key in features]
        # Calculate the weighted sum of features
        weighted_sum = sum(feature * weight for feature, weight in zip(numerical_features, self.weights))
        # Add bias
        weighted_sum += self.bias
        # Apply step function to determine class label
        return 1 if weighted_sum >= 0 else 0

    def update(self, features, label, learning_rate):
        # Predict the label
        prediction = self.predict(features)
        # Update weights and bias based on prediction error
        error = label - prediction
        # Ensure features is a list to avoid TypeError
        numerical_features = [features[key] for key in features]
        self.weights = [weight + learning_rate * error * feature for feature, weight in zip(numerical_features, self.weights)]
        self.bias += learning_rate * error

# Initialize Perceptron with the number of features
perceptron = Perceptron(num_features)

# Train the Perceptron
learning_rate = 0.1
num_epochs = 10


for epoch in range(num_epochs):
    print(f"Epoch {epoch + 1}:")
    for features, label in training_data:
        prediction = perceptron.predict(features)
        print(f"Prediction: {prediction}, Label: {label}")
        perceptron.update(features, label, learning_rate)
