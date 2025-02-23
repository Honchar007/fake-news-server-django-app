# fakenews_server/test_ml_models.py
from django.test import TestCase
from unittest.mock import patch, MagicMock
from .ml_models import load_model


class MLModelsTests(TestCase):
    def setUp(self):
        """Setup mock models and common test data"""
        self.test_text = "This is a test news article"
        self.mock_model = MagicMock()
        self.mock_model.predict.return_value = [1]
        self.mock_model.predict_proba.return_value = [[0.2, 0.8]]

    @patch('joblib.load')
    def test_load_traditional_models(self, mock_joblib_load):
        """Test loading traditional ML models (rf, lr, etc.)"""
        mock_joblib_load.return_value = self.mock_model

        # Test each traditional model
        for model_name in ['rf', 'lr', 'nb', 'svm', 'mlp']:
            model = load_model(model_name)
            self.assertIsNotNone(model)

            # Test prediction
            result = model.predict([self.test_text])
            self.assertEqual(len(result), 1)
            self.assertIn(result[0], [0, 1])

            # Test probability prediction
            proba = model.predict_proba([self.test_text])
            self.assertEqual(len(proba[0]), 2)
            self.assertTrue(0 <= proba[0][0] <= 1)
            self.assertTrue(0 <= proba[0][1] <= 1)

    @patch('transformers.pipeline')
    def test_load_bert_model(self, mock_pipeline):
        """Test loading BERT model"""
        mock_bert = MagicMock()
        mock_bert.return_value = [{'label': 'FAKE', 'score': 0.8}]
        mock_pipeline.return_value = mock_bert

        model = load_model('bert')
        self.assertIsNotNone(model)

        # Test prediction
        result = model.predict([self.test_text])
        self.assertEqual(len(result), 1)
        self.assertIn(result[0], [0, 1])

    def test_empty_input_traditional_model(self):
        """Test prediction with empty input for traditional model"""
        model = load_model('rf')  # Using rf as example
        result = model.predict([''])
        self.assertEqual(len(result), 1)  # Should return single prediction

    def test_empty_input_bert_model(self):
        """Test prediction with empty input for BERT model"""
        model = load_model('bert')
        result = model.predict([''])
        self.assertEqual(len(result), 1)  # Should return single prediction

    @patch('transformers.pipeline')
    def test_bert_prediction_format(self, mock_pipeline):
        """Test BERT prediction format"""
        mock_bert = MagicMock()
        mock_bert.return_value = [{'label': 'FAKE', 'score': 0.8}]
        mock_pipeline.return_value = mock_bert

        model = load_model('bert')
        result = model.predict([self.test_text])

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertIn(result[0], [0, 1])

    @patch('joblib.load')
    def test_traditional_model_format(self, mock_joblib_load):
        """Test traditional model prediction format"""
        mock_joblib_load.return_value = self.mock_model

        model = load_model('rf')
        result = model.predict([self.test_text])

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertIn(result[0], [0, 1])

    @patch('transformers.pipeline')
    def test_bert_probability_format(self, mock_pipeline):
        """Test BERT probability prediction format"""
        mock_bert = MagicMock()
        mock_bert.return_value = [{'label': 'FAKE', 'score': 0.8}]
        mock_pipeline.return_value = mock_bert

        model = load_model('bert')
        if hasattr(model, 'predict_proba'):
            result = model.predict_proba([self.test_text])
            self.assertIsInstance(result[0], list)
            self.assertEqual(len(result[0]), 2)