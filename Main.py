import sys
from FeatureExtraction import extract_features
from Perceptron import Perceptron, num_features, class_labels
from Evaluation import evaluate
import os


def clear_screen():
    """This function clears the console screen."""
    os.system("cls" if os.name == "nt" else "clear")


def display_instructions():
    """This function prints instructions to the user."""
    print("Welcome to the Part-of-speech Tagger Application!")
    print("Here you can discover the POS tags of your sentence.")

# Function to tokenize input sentence
def tokenize_sentence(user_sentence):
    return user_sentence.split()

# Function to predict POS tags for the input sentence
def predict_pos_tags(user_sentence, perceptron):
    words = tokenize_sentence(user_sentence)
    features_for_sentence = list()
    for word in words:
        features_for_sentence.append(extract_features(word))
    print((features_for_sentence))
    pos_tags = [] #the prob is here?
    for features in features_for_sentence:
        pos_tag = perceptron.predict(features)
        pos_tags.append(pos_tag)
    return pos_tags

# Function to display input sentence along with predicted POS tags
def display_results(sentence, pos_tags):
    tokens = tokenize_sentence(sentence)
    for i in range(len(tokens)):
        print(f"{tokens[i]}\t{pos_tags[i]}")


def main():
    """
    This function controls the flow of the program, allowing the enter a new sentence.
    """
    Tagger = None
    while True:
        clear_screen()
        display_instructions()

        # Ask the user if they want to input a new sentence
        if Tagger is None:
            choice = input("Would you like to start? (yes/no): ")
            if choice.lower() != "yes":
                print("Exiting the program. Goodbye!")
                sys.exit()
            user_sentence = input("Please enter the sentence you wish to inspect: ")
            # Initialize Perceptron with the number of features and class labels
            perceptron = Perceptron(num_features, class_labels)
            pos_tags = predict_pos_tags(user_sentence, perceptron)
            display_results(user_sentence, pos_tags)
            
            """
            # Evaluate the model on user sentence
            user_accuracy = evaluate(user_sentence, perceptron)
            print(f"Accuracy on user sentence: {user_accuracy:.2f}%")
            """

        # Exit the program
        print("Exiting the program. Goodbye!")
        sys.exit()


if __name__ == "__main__":
    # Execute the main function if the script is run directly
    main()
