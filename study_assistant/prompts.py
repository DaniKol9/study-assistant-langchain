"""
Prompt templates used throughout the study assistant pipeline.

Prompts are intentionally kept separate from chain logic to improve
readability, maintainability, and prompt iteration.
"""

from langchain_core.prompts import ChatPromptTemplate

MAP_SUMMARY_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "You are a study assistant."),
    ("user", """
Summarize the study material chunk below into concise bullet points.

Study Material Chunk:
{chunk}

Rules:
- Produce 4 to 7 bullet points
- Each bullet must be at most 1 sentence
- Focus on definitions, key ideas, relationships, and examples
- Do not add information that is not present in the text

Output requirements:
- Return ONLY bullet points
- Do not include headings, numbering, or extra text
""")
])


REDUCE_SUMMARY_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "You are a study assistant consolidating notes."),
    ("user", """
Below are bullet-point summaries from multiple sections of the same document.

Chunk Summaries:
{summaries}

Instructions:
- Merge overlapping or duplicated ideas
- Remove redundancy
- Organize bullets in a logical progression
- Produce 10 to 20 final bullet points
- Keep wording clear, concise, and study-friendly

Output requirements:
- Return ONLY the final bullet list
- Do not include headings, numbering, or explanations
""")
])


MCQ_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "You are an educational assessment assistant."),
    ("user", """
Based on the study summary below, generate {num_questions} multiple-choice questions.

Difficulty level: {difficulty}

Difficulty guidelines:
- easy: definition-based or identification questions
- medium: comparison, explanation, or application-based questions
- hard: scenario-based questions, subtle distinctions, or best-answer questions

The difficulty level must strongly influence the style and depth of the questions.

Study Summary:
{summary}

Rules:
- Each question must test a key concept from the summary
- Provide 4 options (A–D)
- Only one correct answer
- Include a brief explanation for the correct answer
- Distractors must be plausible but incorrect
- Avoid obviously wrong or silly options
- For medium and hard questions, avoid trivial or purely definitional questions

Output format requirements:
- Return ONLY valid JSON
- Do NOT include markdown, backticks, or extra text
- The output must be a JSON array of length {num_questions}
- Each element must follow this schema exactly:

[
  {{
    "id": <number>,
    "question": <string>,
    "options": {{
      "A": <string>,
      "B": <string>,
      "C": <string>,
      "D": <string>
    }},
    "correct_answer": "A" | "B" | "C" | "D",
    "explanation": <string>
  }}
]

If the output is not valid JSON, the response is incorrect.
""")
])