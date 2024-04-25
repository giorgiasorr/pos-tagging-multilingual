import re

def preprocess_text(text):
    """
    Preprocess input text by removing noise and stop words, and tokenizing it.
    """
    # Noise removal
    text = re.sub(r"<[^>]+>", "", text)  # Remove HTML tags
    text = re.sub(r"\S*@\S*\s?", "", text)  # Remove emails
    text = re.sub(r"\s+", " ", text)  # Remove extra whitespaces
    text = text.strip()  # Remove leading/trailing whitespaces

    return tokens

def tokenize(text):
    """
    Tokenize input text into a list of tokens.
    """
    # Split text into words and punctuation
    tokens = re.findall(r"\w+|[^\w\s]", text, re.UNICODE)
    return tokens

def detokenize(tokens):
    """
    Detokenize a list of tokens into a string.
    """
    # Joining tokens and handling spaces before punctuations
    text = ' '.join(tokens)
    text = re.sub(r"\s([,.!?;:])", r"\1", text)  # Remove space before punctuations
    return text

# e.g.
if __name__ == "__main__":
    sample_text = "If you shall chance, Camillo, to visit Bohemia, on the like occasion whereon my services are now on foot, you shall see, as I have said, great difference betwixt our Bohemia and your Sicilia. I think, this coming summer, the King of Sicilia means to pay Bohemia the visitation which he justly owes him. Wherein our entertainment shall shame us we will be justified in our loves; for indeed--B"
    
    # Preprocess the text
    tokens = preprocess_text(sample_text)
    
    print("Tokens after preprocessing:", tokens)
    
    # Tokenize the preprocessed text
    tokens = tokenize(" ".join(tokens))
    print("Tokens after tokenization:", tokens)
    
    # Detokenize the tokens
    detokenized_text = detokenize(tokens)
    print("Detokenized:", detokenized_text)
