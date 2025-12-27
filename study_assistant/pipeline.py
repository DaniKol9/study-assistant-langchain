"""
End-to-end orchestration pipeline for generating study MCQs from a PDF.

This module coordinates text loading, preprocessing, summarization (map-reduce),
MCQ generation, and validation into a single reusable function.
"""
from __future__ import annotations

from pathlib import Path
from typing import Literal

from study_assistant.loaders import load_pdf_text
from study_assistant.preprocess import clean_text, repair_newlines
from study_assistant.chains import build_map_chain, build_reduce_chain, build_mcq_chain
from study_assistant.types import Difficulty, MCQList
from study_assistant.validators import validate_mcqs


def run_pdf_to_mcqs(
    pdf_path: str | Path,
    num_questions: int = 8,
    difficulty: Difficulty = "medium",
) -> MCQList:
    """
    Generate validated multiple-choice questions (MCQs) from a PDF document.

    This function implements the full Study Assistant pipeline:
    PDF text extraction → preprocessing → chunking → map–reduce summarization →
    MCQ generation (strict JSON) → parsing → validation.

    Parameters
    ----------
    pdf_path : str or Path
        Path to the input PDF file.
    num_questions : int, optional
        Number of MCQs to generate (default is 8).
    difficulty : {"easy", "medium", "hard"}, optional
        Target difficulty level for generated questions.

    Returns
    -------
    MCQList
        A list of validated MCQ objects (TypedDict-compatible). Each MCQ contains:
        - id (int)
        - question (str)
        - options (A–D)
        - correct_answer ("A" | "B" | "C" | "D")
        - explanation (str)

    Notes
    -----
    - LLM outputs are treated as untrusted input and validated before returning.
    - This function is interface-agnostic and can be reused by the CLI, notebooks,
      or other applications.
    
    Raises
    ------
    AssertionError
        If the generated MCQs fail structural validation.
    """
    # --- 1) Load + preprocess ---
    raw = load_pdf_text(str(pdf_path))
    text = clean_text(repair_newlines(raw))

    # --- 2) Build chains ---
    map_chain, splitter = build_map_chain()
    reduce_chain = build_reduce_chain()
    mcq_chain = build_mcq_chain()

    # --- 3) Chunk + map summarize ---
    chunks = splitter.split_text(text)
    chunk_summaries = [map_chain.invoke({"chunk": c}) for c in chunks]

    # --- 4) Reduce into final summary ---
    final_summary = reduce_chain.invoke({"summaries": "\n\n".join(chunk_summaries)})

    # --- 5) Generate MCQs as structured JSON ---
    mcqs = mcq_chain.invoke(
        {
            "summary": final_summary,
            "num_questions": num_questions,
            "difficulty": difficulty,
        }
    )

    # --- 6) Validate shape/keys before returning ---
    validate_mcqs(mcqs, expected_n=num_questions)
    return mcqs