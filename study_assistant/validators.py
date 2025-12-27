"""
Validation utilities for LLM-generated outputs.

LLM outputs are treated as untrusted and validated before downstream use.
"""
from study_assistant.types import MCQList

def validate_mcqs(mcqs: MCQList, expected_n: int) -> None:
    """
    Minimal validation: treat LLM output as untrusted.
    Raises AssertionError if the shape is wrong.
    """
    assert isinstance(mcqs, list), "MCQs must be a list"
    assert len(mcqs) == expected_n, f"Expected {expected_n} MCQs, got {len(mcqs)}"

    for q in mcqs:
        assert isinstance(q, dict), "Each MCQ must be a dict"
        for key in ("id", "question", "options", "correct_answer", "explanation"):
            assert key in q, f"Missing key: {key}"

        options = q["options"]
        assert isinstance(options, dict), "options must be a dict"
        assert set(options.keys()) == {"A", "B", "C", "D"}, "options must have A-D"

        correct = q["correct_answer"]
        assert correct in {"A", "B", "C", "D"}, "correct_answer must be A/B/C/D"
        assert options[correct].strip() != "", "Correct option text must be non-empty"
        assert str(q["explanation"]).strip() != "", "Explanation must be non-empty"