import os
import time
from langchain_groq import ChatGroq

judge_llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY"),
)


def _call_with_retry(prompt: str) -> str:
    for attempt in range(5):
        try:
            response = judge_llm.invoke(prompt)
            return response.content.strip().upper()
        except Exception as e:
            if "rate_limit" in str(e).lower() or "429" in str(e):
                wait = 15 * (attempt + 1)
                print(f"    [rate limit] waiting {wait}s...")
                time.sleep(wait)
            else:
                raise
    return ""


def judge_all(question: str, answer: str, expected: str) -> dict:
    """Single LLM call for all 3 metrics."""
    prompt = f"""You are an evaluator. Answer all 3 questions with YES or NO only.

Question: {question}
Expected Answer: {expected}
Given Answer: {answer}

1. HALLUCINATION: Does the Given Answer contain facts NOT in the Expected Answer or clearly wrong facts?
2. RELEVANCY: Is the Given Answer relevant and on-topic for the question?
3. FAITHFULNESS: Does the Given Answer faithfully cover the main points of the Expected Answer?

Reply in exactly this format:
HALLUCINATION: YES or NO
RELEVANCY: YES or NO
FAITHFULNESS: YES or NO"""

    raw = _call_with_retry(prompt)

    def extract(label):
        for line in raw.splitlines():
            if label in line:
                return "YES" in line
        return False

    return {
        "hallucinated": extract("HALLUCINATION"),
        "relevant": extract("RELEVANCY"),
        "faithful": extract("FAITHFULNESS"),
    }


def compute_latency_stats(latencies: list) -> dict:
    arr = sorted(latencies)
    n = len(arr)
    p50 = arr[n // 2]
    p95 = arr[min(int(n * 0.95), n - 1)]
    return {"p50_ms": round(p50, 1), "p95_ms": round(p95, 1)}
