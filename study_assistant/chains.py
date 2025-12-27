"""
LangChain chain builders for the study assistant.

Each function in this module constructs a specific chain (map, reduce, MCQ)
with its appropriate prompt, LLM configuration, and output parser.
"""
from __future__ import annotations

from langchain_openai import ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser

from study_assistant.prompts import MAP_SUMMARY_PROMPT, REDUCE_SUMMARY_PROMPT, MCQ_PROMPT


def get_llm():
    """Create a deterministic chat model (temperature=0) for consistent outputs."""
    return ChatOpenAI(model="gpt-4o-mini", temperature=0)


def build_map_chain():
    """Chunk summarization returns bullet text, so we use StrOutputParser."""
    llm = get_llm()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=150)
    chain = MAP_SUMMARY_PROMPT | llm | StrOutputParser()
    return chain, splitter


def build_reduce_chain():
    """Reduce step returns bullet text, so we use StrOutputParser."""
    llm = get_llm()
    return REDUCE_SUMMARY_PROMPT | llm | StrOutputParser()


def build_mcq_chain():
    """MCQ step returns JSON, so we use JsonOutputParser."""
    llm = get_llm()
    return MCQ_PROMPT | llm | JsonOutputParser()