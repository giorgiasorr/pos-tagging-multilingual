def extract_features(word, prev_word=None, next_word=None):
    features = {}
    features['word'] = word
    features['prefix'] = word[:3]  # Extract 1st 3 characters as prefix
    features['suffix'] = word[-3:]  # Extract last 3 characters as suffix
    features['is_upper'] = word.isupper()  # uppercasing
    features['is_digit'] = word.isdigit()  # for digits
    features['has_hyphen'] = '-' in word  # for hyphens
    features['has_apostrophe'] = "'" in word  # for apostrophe
    features['prev_word'] = prev_word
    features['next_word'] = next_word
    return features
