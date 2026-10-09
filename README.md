# SWYNEX Final AI Application — Student Feedback Classifier

**SWYNEX Technologies Internship · Task 4 · Beginner-friendly final project**

A small, explainable machine-learning application that classifies student or intern feedback into a useful category. It brings together the problem definition, model integration, confidence-aware review workflow, demo, evaluation, limitations, and ethics notes from the earlier project stages.

> **Prototype notice:** This is an educational demonstration built with a tiny, hand-written sample dataset. It is not validated for real operational decisions, and the reported hold-out score should not be interpreted as evidence of production readiness.

## 1. Problem

Student and internship feedback can arrive as free-form text. Manually sorting every message can be time-consuming. This project demonstrates how a basic NLP classifier can suggest a category to help organize incoming feedback.

### Categories

- **Positive Feedback** — praise or a positive experience.
- **Negative Feedback** — dissatisfaction or a generally negative experience.
- **Question** — asks for information or clarification.
- **Suggestion** — proposes an improvement.
- **Complaint** — reports a specific problem that needs attention.

These labels can overlap in real conversations. A person should make the final decision whenever the intent is unclear or the outcome matters.

## 2. Method

The app uses a scikit-learn text-classification pipeline:

1. **Input validation:** rejects blank feedback and messages longer than 2,000 characters.
2. **TF-IDF features:** converts words and two-word phrases into numeric features, giving more weight to terms that help distinguish messages.
3. **Logistic Regression:** learns to associate those features with the five feedback categories.
4. **Confidence estimate:** returns the largest class probability as a confidence-like score.
5. **Human-review routing:** flags a prediction when that score is below a configurable threshold (default: 0.45).

The dataset is split into training and held-out test sets using a stratified 75/25 split with a fixed random seed. The CLI reports accuracy, Macro-F1, and a per-class precision/recall report. The evaluation script also checks selected examples and input validation.

**Important:** model probabilities can be poorly calibrated. A score is not a guarantee that the prediction is correct, and high confidence does not remove the need for human judgment.

## 3. Quick start

Requires Python 3.10 or newer.

### Install

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate

python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Run the command-line demo

```bash
python src/app.py
```

Classify your own feedback:

```bash
python src/app.py --text "Could you explain the deadline for the next task?"
```

Change the threshold for human review:

```bash
python src/app.py --text "The portal is confusing" --threshold 0.60
```

The application trains from the included CSV whenever it runs; it does not download a pretrained model or require an API key.

### Run the optional web interface

```bash
streamlit run src/streamlit_app.py
```

Type a feedback message, adjust the review threshold, and select **Classify feedback**.

### Run evaluation examples

```bash
python src/evaluate.py
```

## 4. Demo

Example messages and their intended categories:

| Example feedback | Intended category |
|---|---|
| “The mentor session was useful and well organized.” | Positive Feedback |
| “When is the next task due?” | Question |
| “Please add a calendar for deadlines.” | Suggestion |
| “My submitted task disappeared from the portal.” | Complaint |
| “Blue quickly the window although tomorrow.” | Ambiguous / out of domain; inspect manually |

The exact prediction and score depend on the trained model and dataset. Ambiguous or nonsensical text should not be treated as a reliable classification just because the model returns a category.

## 5. Project structure

```text
SWYNEX-Final-AI-Application/
├── README.md
├── requirements.txt
├── .gitignore
├── LICENSE
├── data/
│   └── sample_feedback.csv
├── docs/
│   └── ETHICS_AND_LIMITATIONS.md
├── examples/
│   └── evaluation_cases.json
├── src/
│   ├── feedback_model.py
│   ├── app.py
│   ├── evaluate.py
│   └── streamlit_app.py
└── tests/
    └── test_feedback_model.py
```

## 6. Evaluation and results

On each run, the app trains on 75% of the sample data and reports results on the remaining 25%. It prints:

- **Accuracy:** share of test examples classified correctly.
- **Macro-F1:** average F1 across classes, giving each class equal weight.
- **Precision and recall:** per-class measures shown in the classification report.
- **Curated-case checks:** compares a few known examples and exercises invalid-input handling.

The sample data contains only 50 short, synthetic examples (10 per category). A small test split has high variance; the same or similar wording may appear in both the limited training and test examples. No benchmark result is claimed here as a production-quality score. Run the evaluation locally to see the actual metrics generated by the current code.

## 7. Limitations

- The dataset is small, synthetic, and not representative of all students, languages, writing styles, or institutions.
- The model mostly learns surface-level word patterns; it may miss sarcasm, context, mixed intent, spelling errors, and domain-specific wording.
- Some categories overlap, especially negative feedback and complaints.
- TF-IDF and Logistic Regression are a simple baseline, not a semantic language model.
- The highest class probability is not necessarily calibrated confidence.
- The review threshold is a configurable demonstration value, not a scientifically established safety boundary.
- Retraining happens at application startup; there is no model registry, monitoring, database, authentication, or production deployment configuration.
- Evaluation on a tiny held-out set is not enough to establish real-world reliability.

## 8. Ethics, privacy, and responsible use

- **Human oversight:** treat predictions as suggestions. Have a person review uncertain, sensitive, or consequential messages.
- **No automated penalties:** do not use this demo to rank students, deny opportunities, evaluate performance, or take disciplinary action.
- **Privacy:** do not enter names, contact details, grades, health information, or other sensitive personal data. Use anonymized text for experimentation.
- **Bias and coverage:** collect consented, representative examples before any real use; check errors across language and writing-style groups where appropriate.
- **Transparency:** tell users when an automated classifier is involved and explain that errors are possible.
- **Data quality:** obtain permission to use feedback, remove identifiers, review labels, and maintain a documented process for correcting mistakes.
- **Security:** this repository requires no secrets or external API keys. Do not commit credentials or real personal feedback.

More detail is available in [docs/ETHICS_AND_LIMITATIONS.md](docs/ETHICS_AND_LIMITATIONS.md).

## 9. Tests

Run the basic unit tests with:

```bash
python -m unittest discover -s tests -v
```

## 10. Learning outcomes

This project demonstrates a complete beginner-friendly AI workflow: defining a classification problem, preparing labeled examples, integrating an NLP model, reporting evaluation metrics, validating input, surfacing uncertainty, routing low-confidence predictions to people, and documenting limitations and ethical safeguards.

## 11. License

Released under the MIT License. See [LICENSE](LICENSE).
