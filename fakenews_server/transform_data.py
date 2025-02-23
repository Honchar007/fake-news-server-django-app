import numpy as np
import re
import joblib

# Load the trained vectorizer
vectorizer = joblib.load('models_v1/tfidf_combined_improved.pkl')  # Adjust the path as needed

def preprocess_input(title, text):
    # Combine title and text into a single input
    combined_text = f"{title} {text}"

    # Clean the text
    combined_text = re.sub(r'\W', ' ', combined_text)  # Remove non-word characters
    combined_text = re.sub(r'\s+', ' ', combined_text).strip()  # Replace multiple spaces with a single space
    combined_text = combined_text.lower()  # Convert to lowercase

    # Transform the cleaned text into features using the vectorizer
    features = vectorizer.transform([combined_text]).toarray()

    return features[0]  # Return the features as a 1D array
