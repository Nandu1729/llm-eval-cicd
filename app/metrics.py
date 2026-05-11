import os
from langchain_groq import ChatGroq

judge_llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY"),
)


def _judge(prompt: str) -> bool:
    response = judge_llm.invoke(prompt)
    return "YES" in response.content.strip().upper()


def check_hallucination(question: str, answer: str, expected: str) -> bool:
    prompt = f"""You are a strict fact-checker.

Question: {question}
Expected Answer: {expected}
Given Answer: {answer}

Does the Given Answer contain facts that are NOT in the Expected Answer or are clearly wrong?
Reply ONLY: YES (hallucination detected) or NO (no hallucination)."""
    return _judge(prompt)


def check_relevancy(question: str, answer: str) -> bool:
    prompt = f"""Question: {question}
Answer: {answer}

Is this answer relevant and on-topic for the question?
Reply ONLY: YES or NO."""
    return _judge(prompt)


def check_faithfulness(question: str, answer: str, expected: str) -> bool:
    prompt = f"""Question: {question}
Expected Answer: {expected}
Given Answer: {answer}

Does the Given Answer faithfully cover the main points of the Expected Answer without contradicting it?
Reply ONLY: YES or NO."""
    return _judge(prompt)


def compute_latency_stats(latencies: list) -> dict:
    arr = sorted(latencies)
    n = len(arr)
    p50 = arr[n // 2]
    p95 = arr[min(int(n * 0.95), n - 1)]
    return {"p50_ms": round(p50, 1), "p95_ms": round(p95, 1)}
