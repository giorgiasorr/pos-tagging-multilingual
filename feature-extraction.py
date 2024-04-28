def extract_features(word, prev_word=None, next_word=None):
    features = {}
    features['word'] = word
    features['prefix'] = word[:3]  # Extract first three characters as prefix
    features['suffix'] = word[-3:]  # Extract last three characters as suffix
    features['is_upper'] = word.isupper()  # True if all characters are uppercase
    features['is_digit'] = word.isdigit()  # True if all characters are digits
    features['has_hyphen'] = '-' in word  # True if word contains a hyphen
    features['has_apostrophe'] = "'" in word  # True if word contains an apostrophe
    features['prev_word'] = prev_word
    features['next_word'] = next_word
    return features
