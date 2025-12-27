"""
Command-line interface for the study assistant which generates MCQs from a PDF.

Provides a user-friendly wrapper around the reusable pipeline with
configurable parameters.

Example:
python -m study_assistant.cli \
  --pdf sample_input/Prompt_Engineering.pdf \
  --num-questions 5 \
  --difficulty medium
"""

from pathlib import Path
import argparse
from dotenv import load_dotenv

from study_assistant.pipeline import run_pdf_to_mcqs


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(description="Generate MCQs from a PDF.")
    parser.add_argument(
        "--pdf",
        type=Path,
        required=True,
        help="Path to the PDF file",
    )
    parser.add_argument(
        "--num-questions",
        type=int,
        default=8,
        help="Number of MCQs to generate",
    )
    parser.add_argument(
        "--difficulty",
        choices=["easy", "medium", "hard"],
        default="medium",
        help="Difficulty level of the MCQs",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Optional path to write MCQs as a JSON file (e.g. sample_output/example_mcqs.json)",
    )
    return parser.parse_args()


def main() -> None:
    """CLI entrypoint."""
    load_dotenv()  # Load API keys from .env
    args = parse_args()

    mcqs = run_pdf_to_mcqs(
        pdf_path=args.pdf,
        num_questions=args.num_questions,
        difficulty=args.difficulty,
    )

    import json
    if args.out is not None:
        # Ensure parent directory exists (e.g. sample_output/)
        args.out.parent.mkdir(parents=True, exist_ok=True)

        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(mcqs, f, indent=2)

        print(f"MCQs written to {args.out}")
    else:
        # Fallback: print to stdout
        for q in mcqs:
            print(json.dumps(q, indent=2))
            print("-" * 40)


if __name__ == "__main__":
    main()