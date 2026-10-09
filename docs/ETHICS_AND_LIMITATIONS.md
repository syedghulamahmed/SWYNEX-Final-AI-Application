# Ethics and Limitations

This project is an educational prototype for student/internship feedback triage. It must not be treated as a reliable decision-making system.

## Responsible use

- Treat the predicted category as a suggestion, not a fact.
- Require human review for uncertain, sensitive, disputed, or consequential messages.
- Never use the demo to grade students, rank interns, deny opportunities, or make disciplinary decisions.
- Do not enter names, contact details, grades, health information, or other sensitive personal data.
- If adapting the project, use feedback collected with appropriate permission, remove identifiers, and explain to participants how automated classification is used.
- Review model errors and label quality. The categories can overlap, and a small or unrepresentative dataset can create systematic errors.
- Be transparent that predictions may be wrong and provide a way for people to correct them.
- Keep credentials and private information out of the repository. This app does not need API keys.

## Technical limitations

- Only 50 synthetic examples are included, with 10 per category.
- A single stratified test split on a small dataset is noisy and not enough to demonstrate generalization.
- TF-IDF relies on word and phrase patterns; it may struggle with sarcasm, negation, context, multilingual messages, typos, and mixed intent.
- The highest predicted class probability is called a confidence estimate in the interface. It may not be calibrated.
- The threshold of 0.45 is a configurable demonstration default, not a validated safety threshold.
- Out-of-domain messages are still assigned one of the known labels unless a separate rejection mechanism is developed and validated.

## Before any real deployment

Collect a larger and representative consented dataset; define label guidelines; obtain expert-reviewed annotations; use repeated or cross-validation evaluation; check performance across relevant language and demographic groups where lawful and appropriate; calibrate probabilities; establish monitoring and an appeal/correction process; and complete a privacy/security review.
