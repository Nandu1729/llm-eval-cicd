import os
import time
from langchain_groq import ChatGroq

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.3,
    api_key=os.getenv("GROQ_API_KEY"),
)

INPUT_TOKEN_COST = 0.05 / 1_000_000   # $0.05 per 1M tokens
OUTPUT_TOKEN_COST = 0.08 / 1_000_000  # $0.08 per 1M tokens


def call_llm(question: str) -> dict:
    for attempt in range(5):
        try:
            start = time.time()
            response = llm.invoke(question)
            latency_ms = (time.time() - start) * 1000
            content = response.content.strip()
            break
        except Exception as e:
            if "rate_limit" in str(e).lower() or "429" in str(e):
                wait = 15 * (attempt + 1)
                print(f"    [rate limit] waiting {wait}s...")
                time.sleep(wait)
            else:
                raise

    input_tokens = len(question.split()) * 1.3
    output_tokens = len(content.split()) * 1.3
    cost = (input_tokens * INPUT_TOKEN_COST) + (output_tokens * OUTPUT_TOKEN_COST)

    return {
        "answer": content,
        "latency_ms": latency_ms,
        "cost_usd": cost,
    }
