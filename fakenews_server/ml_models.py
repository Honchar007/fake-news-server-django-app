# ml_models.py
import joblib
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch


class BERTPredictor:
    def __init__(self, model, tokenizer):
        self.model = model
        self.tokenizer = tokenizer
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        self.model.eval()

    def predict(self, text):
        # text should be raw text, not vectorized features
        if isinstance(text, list) and len(text) == 1:
            text = text[0]  # Extract the text from the list

        with torch.no_grad():
            inputs = self.tokenizer(
                text,
                truncation=True,
                padding=True,
                max_length=512,
                return_tensors="pt"
            ).to(self.device)

            outputs = self.model(**inputs)
            predictions = torch.softmax(outputs.logits, dim=1)
            return (predictions[:, 1] > 0.5).cpu().numpy()

    def predict_proba(self, text):
        if isinstance(text, list) and len(text) == 1:
            text = text[0]  # Extract the text from the list

        with torch.no_grad():
            inputs = self.tokenizer(
                text,
                truncation=True,
                padding=True,
                max_length=512,
                return_tensors="pt"
            ).to(self.device)

            outputs = self.model(**inputs)
            predictions = torch.softmax(outputs.logits, dim=1)
            return predictions.cpu().numpy()


def load_model(model_name):
    """Load the specified ML model"""
    model_paths = {
        'rf': 'models_v1/rf_combined_improved.pkl',
        'lr': 'models_v1/lr_combined_improved.pkl',
        'nb': 'models_v1/nb_combined_improved.pkl',
        'mlp': 'models_v1/mlp_combined_improved.pkl',
        'svm': 'models_v1/svm_combined_improved.pkl',
        'bert': 'models_v1/fake_news_detector_final'
    }

    if model_name not in model_paths:
        raise ValueError(f"Unknown model: {model_name}")

    if model_name == 'bert':
        # Load BERT model and tokenizer
        model = AutoModelForSequenceClassification.from_pretrained(model_paths[model_name])
        tokenizer = AutoTokenizer.from_pretrained(model_paths[model_name])
        return BERTPredictor(model, tokenizer)
    else:
        # Load traditional ML models
        return joblib.load(model_paths[model_name])