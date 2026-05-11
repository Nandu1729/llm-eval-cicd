from app.dataset import load_golden_dataset
from app.llm_call import call_llm
from app.metrics import check_hallucination, check_relevancy, check_faithfulness


def run_evaluation(dataset=None):
    if dataset is None:
        dataset = load_golden_dataset()

    results = []
    total = len(dataset)
    print(f"\n  Running eval on {total} samples...\n")

    for i, item in enumerate(dataset, 1):
        question = item["question"]
        expected = item["expected_answer"]

        print(f"  [{i:02d}/{total}] {question[:55]}...")

        llm_result = call_llm(question)
        answer = llm_result["answer"]

        hallucinated = check_hallucination(question, answer, expected)
        relevant = check_relevancy(question, answer)
        faithful = check_faithfulness(question, answer, expected)

        results.append({
            "id": item.get("id", f"q{i:03d}"),
            "category": item.get("category", "general"),
            "question": question,
            "expected": expected,
            "answer": answer,
            "latency_ms": llm_result["latency_ms"],
            "cost_usd": llm_result["cost_usd"],
            "hallucinated": hallucinated,
            "relevant": relevant,
            "faithful": faithful,
        })

    return results
