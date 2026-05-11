import yaml
import os


def load_thresholds(path=None):
    if path is None:
        path = os.path.join(os.path.dirname(__file__), "..", "config.yaml")
    with open(path) as f:
        return yaml.safe_load(f).get("thresholds", {})


def evaluate_gate(summary: dict) -> dict:
    t = load_thresholds()

    hallucination_failed = summary["hallucination_rate"] > t.get("max_hallucination_rate", 0.05)
    relevancy_failed = summary["relevancy_score"] < t.get("min_relevancy_score", 0.80)
    faithfulness_failed = summary["faithfulness_score"] < t.get("min_faithfulness_score", 0.75)
    latency_failed = summary["latency_p95_ms"] > t.get("max_p95_latency_ms", 5000)

    passed = not any([hallucination_failed, relevancy_failed, faithfulness_failed, latency_failed])

    return {
        "passed": passed,
        "hallucination_failed": hallucination_failed,
        "relevancy_failed": relevancy_failed,
        "faithfulness_failed": faithfulness_failed,
        "latency_failed": latency_failed,
    }
