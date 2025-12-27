"""
Shared type definitions for the Study Assistant package.

This module centralizes strongly-typed schemas used across the pipeline,
including MCQ structures, option keys, and difficulty levels.

Using TypedDict-based models improves readability, editor autocomplete, and
helps keep the JSON output schema stable as the project evolves.
"""

from __future__ import annotations

from typing import TypedDict, Literal, Dict, List

Difficulty = Literal["easy", "medium", "hard"]
AnswerLetter = Literal["A", "B", "C", "D"]


class MCQOptions(TypedDict):
    A: str
    B: str
    C: str
    D: str


class MCQ(TypedDict):
    id: int
    question: str
    options: MCQOptions
    correct_answer: AnswerLetter
    explanation: str


MCQList = List[MCQ]