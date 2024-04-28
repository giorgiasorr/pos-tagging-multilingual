import random

class Perceptron:
    def __init__(self, num_features):
        # Initialize weights with random values between 0 and 1
        self.weights = [random.uniform(0, 1) for _ in range(num_features)]
        # Initialize bias with a random value between 0 and 1
        self.bias = random.uniform(0, 1)

    def predict(self, features):
        # Calculate the weighted sum of features
        weighted_sum = sum(feature * weight for feature, weight in zip(features, self.weights))
        # Add bias
        weighted_sum += self.bias
        # Apply step function to determine class label
        return 1 if weighted_sum >= 0 else 0

    def update(self, features, label, learning_rate):
        # Predict the label
        prediction = self.predict(features)
        # Update weights and bias based on prediction error
        error = label - prediction
        self.weights = [weight + learning_rate * error * feature for feature, weight in zip(features, self.weights)]
        self.bias += learning_rate * error
