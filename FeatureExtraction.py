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