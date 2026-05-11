from app.dataset import load_golden_dataset
from app.llm_call import call_llm
from app.metrics import judge_all


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

        scores = judge_all(question, answer, expected)

        results.append({
            "id": item.get("id", f"q{i:03d}"),
            "category": item.get("category", "general"),
            "question": question,
            "expected": expected,
            "answer": answer,
            "latency_ms": llm_result["latency_ms"],
            "cost_usd": llm_result["cost_usd"],
            "hallucinated": scores["hallucinated"],
            "relevant": scores["relevant"],
            "faithful": scores["faithful"],
        })

    return results
