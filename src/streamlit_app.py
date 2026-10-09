from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from feedback_model import classify, train_and_evaluate  # noqa: E402

st.set_page_config(page_title="Student Feedback Triage", page_icon="🧠", layout="centered")
st.title("Student Feedback Triage")
st.write("Classify a feedback message and flag uncertain predictions for human review.")


@st.cache_resource
def get_model():
    return train_and_evaluate()


try:
    model, metrics = get_model()
    st.caption(
        f"Demo hold-out accuracy: {metrics['accuracy']:.1%} · "
        f"Macro-F1: {metrics['macro_f1']:.3f}"
    )
except Exception as exc:
    st.error(f"Model could not be loaded: {exc}")
    st.stop()

message = st.text_area(
    "Feedback message",
    placeholder="Type a short feedback message…",
    max_chars=2000,
)
threshold = st.slider("Human-review confidence threshold", 0.10, 0.95, 0.45, 0.05)

if st.button("Classify feedback", type="primary"):
    try:
        result = classify(model, message, threshold)
        st.subheader("Result")
        st.write(f"**Category:** {result['category']}")
        st.write(f"**Confidence estimate:** {result['confidence']:.1%}")
        if result["needs_human_review"]:
            st.warning(result["review_reason"] + " Please check the message manually.")
        else:
            st.success("Above the selected threshold; a human check may still be appropriate.")
        st.info(
            "This is a small educational prototype. Confidence is not a guarantee of correctness."
        )
    except ValueError as exc:
        st.error(str(exc))
