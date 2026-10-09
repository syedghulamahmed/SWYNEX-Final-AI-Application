from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from feedback_model import build_model, classify, load_data  # noqa: E402


class FeedbackModelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        texts, labels = load_data()
        cls.model = build_model()
        cls.model.fit(texts, labels)

    def test_dataset_has_expected_categories(self):
        _, labels = load_data()
        self.assertEqual(set(labels.unique()), {
            "Positive Feedback", "Negative Feedback", "Question", "Suggestion", "Complaint"
        })

    def test_classification_returns_valid_category_and_score(self):
        result = classify(self.model, "The mentor session was helpful.")
        self.assertIn(result["category"], self.model.classes_)
        self.assertGreaterEqual(result["confidence"], 0.0)
        self.assertLessEqual(result["confidence"], 1.0)

    def test_empty_input_is_rejected(self):
        with self.assertRaises(ValueError):
            classify(self.model, "")

    def test_whitespace_input_is_rejected(self):
        with self.assertRaises(ValueError):
            classify(self.model, "   ")

    def test_overlong_input_is_rejected(self):
        with self.assertRaises(ValueError):
            classify(self.model, "x" * 2001)

    def test_invalid_threshold_is_rejected(self):
        with self.assertRaises(ValueError):
            classify(self.model, "Hello", 1.1)


if __name__ == "__main__":
    unittest.main()
