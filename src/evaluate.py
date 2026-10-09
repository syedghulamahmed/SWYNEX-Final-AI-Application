from __future__ import annotations

import json
from pathlib import Path

from feedback_model import classify, train_and_evaluate

ROOT = Path(__file__).resolve().parents[1]
CASES_PATH = ROOT / "examples" / "evaluation_cases.json"


def main() -> int:
    try:
        model, metrics = train_and_evaluate()
        cases = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print(f"Evaluation setup failed: {exc}")
        return 1

    print("\nCurated evaluation cases")
    correct = scored = 0
    for case in cases:
        message = case["input"]
        expected = case.get("expected_category")
        if not message.strip():
            try:
                classify(model, message)
                actual = "UNEXPECTED ACCEPT"
                passed = False
            except ValueError as exc:
                actual = f"REJECTED: {exc}"
                passed = True
            print(f"[{'PASS' if passed else 'FAIL'}] {case['name']}: {actual}")
            continue
        result = classify(model, message)
        passed = expected is None or result["category"] == expected
        if expected is not None:
            scored += 1
            correct += int(passed)
        print(f"[{'PASS' if passed else 'REVIEW'}] {case['name']}")
        print(f"  Expected: {expected or 'Ambiguous / inspect manually'}")
        print(f"  Predicted: {result['category']} ({result['confidence']:.3f})")
        print(f"  Human review flag: {result['needs_human_review']}")
        print(f"  Note: {case['purpose']}")
    print("\nSummary")
    print(f"Hold-out accuracy: {metrics['accuracy']:.3f}")
    print(f"Hold-out macro-F1: {metrics['macro_f1']:.3f}")
    if scored:
        print(f"Curated labeled-case agreement: {correct}/{scored} ({correct/scored:.1%})")
    print("Ambiguous cases are qualitative checks, not a scored benchmark.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
