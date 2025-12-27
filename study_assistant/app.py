"""
Minimal demonstration entry point for the Study Assistant package.

This module runs the end-to-end PDF-to-MCQ pipeline against a sample input
document for quick sanity checks and development testing.

It is intentionally lightweight:
- All core logic lives in `pipeline.py`
- User-facing execution is handled by `cli.py`

For most use cases, prefer running the CLI:
    python -m study_assistant.cli

Run this module using:
    python -m study_assistant.app
"""

from pathlib import Path
from dotenv import load_dotenv

from study_assistant.pipeline import run_pdf_to_mcqs

load_dotenv()

if __name__ == "__main__":
    pdf_path = (
        Path(__file__).resolve().parent.parent
        / "sample_input"
        / "Prompt_Engineering.pdf"
    )
    mcqs = run_pdf_to_mcqs(pdf_path, num_questions=5, difficulty="medium")
    print(f"Generated {len(mcqs)} MCQs from sample input.")
