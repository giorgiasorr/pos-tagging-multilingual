def extract_features(word, prev_word=None, next_word=None):
    features = {}
    features['word'] = float(ord(word[0]))  # Using ascii value of the 1st character 
    features['prefix'] = float(ord(word[0]))  #  1st character 
    features['suffix'] = float(ord(word[-1]))  # the last character 
    features['is_upper'] = float(word.isupper())  # Convert boolean to float
    features['is_digit'] = float(word.isdigit())  # Convert boolean to float
    features['has_hyphen'] = float('-' in word)  # Convert boolean to float
    features['has_apostrophe'] = float("'" in word)  # Convert boolean to float
    features['prev_word'] = float(ord(prev_word[0])) if prev_word else 0  # ascii of the 1st character as a numerical representation if prev_word is not None
    features['next_word'] = float(ord(next_word[0])) if next_word else 0  # 1st character as a numerical representation if next_word is not None
    return features
