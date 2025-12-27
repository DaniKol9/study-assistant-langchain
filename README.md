# Study Assistant — PDF to MCQ Generator (LangChain)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
A reusable LangChain-based pipeline that converts a PDF document into
exam-ready multiple-choice questions (MCQs).

The system performs:
- PDF text extraction
- Text cleaning and chunking
- Map–reduce summarization
- Parameterized MCQ generation (difficulty + count)
- Structured JSON output + parsing
- Validation of LLM outputs before downstream use

---

## Features

- End-to-end PDF → MCQ pipeline
- Reusable Python package (not a one-off script)
- Configurable question count and difficulty
- Strict JSON schema for reliable downstream use (UI, grading, storage)
- Typed MCQ schema (`TypedDict`) for readability and autocomplete
- Command-line interface (CLI)
- Designed with production-grade LangChain patterns

---

## Project Structure
```
study_assistant/
├── init.py
├── app.py          # Minimal demo entrypoint
├── cli.py          # Command-line interface
├── pipeline.py     # End-to-end orchestration (public API)
├── chains.py       # LangChain chain builders (prompt + LLM + parser)
├── prompts.py      # Prompt templates
├── loaders.py      # PDF loading utilities
├── preprocess.py   # Text cleanup utilities
├── validators.py   # LLM output validation
├── types.py        # Typed MCQ schema + shared type aliases
```
---

## Installation

1. Create and activate a virtual environment with Python 3.11+
2. Install dependencies:

```bash
pip install -r requirements.txt
```
3.	Add your OpenAI API key to a .env file:

OPENAI_API_KEY=your_key_here

Tested with Python 3.11+
---

## Usage

### Run via CLI

The `sample_input/` folder contains an example PDF used for development and
demonstration. The pipeline works with any user-provided PDF.

Generate MCQs from a PDF and optionally write them to a JSON file:
```bash
python -m study_assistant.cli \
  --pdf sample_input/Prompt_Engineering.pdf \
  --num-questions 10 \
  --difficulty hard \
  --out sample_output/example_mcqs.json
```
If --out is not provided, MCQs are printed to standard output.

### Use as a Python module
```python
from study_assistant.pipeline import run_pdf_to_mcqs

mcqs = run_pdf_to_mcqs(
    pdf_path="document.pdf",
    num_questions=5,
    difficulty="medium",
)
```

---

## Output Format

MCQs are returned as structured JSON-compatible dictionaries that match the
typed schema defined in study_assistant/types.py.
Example:
```json
[
  {
    "id": 1,
    "question": "...",
    "options": {
      "A": "...",
      "B": "...",
      "C": "...",
      "D": "..."
    },
    "correct_answer": "B",
    "explanation": "..."
  }
]
```
---
## Design Notes

- **Map–reduce summarization:**  
  The pipeline uses a map–reduce pattern (chunk-level summaries followed by a
  reduction step) to handle longer documents reliably and mitigate context-window
  limitations of LLMs.

- **Per-chain output parsers:**  
  Each LangChain chain owns its output contract and parser:
  summarization chains use text output parsing, while the MCQ generation chain
  uses strict JSON parsing. This avoids ambiguity and enforces clear boundaries
  between stages.

- **Structured output + validation:**  
  MCQs are generated as strict JSON-compatible data and validated before being
  returned. LLM outputs are treated as untrusted input to ensure downstream
  reliability.

- **Separation of concerns:**  
  Core pipeline logic is isolated in `pipeline.py`, while interfaces such as the
  CLI handle input/output concerns (e.g. writing JSON files). This makes the
  system reusable across different entrypoints.

- **Typed schemas for MCQs:**  
  Shared type definitions (`TypedDict`) are used to document and stabilize the
  MCQ schema, improving readability, editor support, and future extensibility.
---
## Future Improvements
	•	Automatic retries on validation failure
	•	Support for additional document types
	•	UI or web interface
	•	Question difficulty calibration
	•	Unit tests for prompts and validators

---

## License

This project is licensed under the MIT License.

---
