from app.metrics import compute_latency_stats

W = 58


def compute_summary(results: list) -> dict:
    n = len(results)
    latency_stats = compute_latency_stats([r["latency_ms"] for r in results])

    return {
        "total_samples": n,
        "hallucination_rate": sum(1 for r in results if r["hallucinated"]) / n,
        "relevancy_score": sum(1 for r in results if r["relevant"]) / n,
        "faithfulness_score": sum(1 for r in results if r["faithful"]) / n,
        "latency_p50_ms": latency_stats["p50_ms"],
        "latency_p95_ms": latency_stats["p95_ms"],
        "total_cost_usd": sum(r["cost_usd"] for r in results),
        "avg_cost_per_query_usd": sum(r["cost_usd"] for r in results) / n,
    }


def print_dashboard(summary: dict, gate_result: dict):
    print("\n" + "═" * W)
    print("   LLM Eval CI/CD  —  Results Dashboard")
    print("═" * W)
    print(f"\n  Samples evaluated : {summary['total_samples']}")
    print(f"\n  {'METRIC':<32} {'VALUE':<12} STATUS")
    print("  " + "─" * (W - 2))

    def row(label, value, ok):
        status = "PASS" if ok else "FAIL"
        print(f"  {label:<32} {value:<12} {status}")

    row("Hallucination Rate",
        f"{summary['hallucination_rate']*100:.1f}%",
        not gate_result["hallucination_failed"])

    row("Answer Relevancy",
        f"{summary['relevancy_score']*100:.1f}%",
        not gate_result["relevancy_failed"])

    row("Faithfulness",
        f"{summary['faithfulness_score']*100:.1f}%",
        not gate_result["faithfulness_failed"])

    row("Latency p50",
        f"{summary['latency_p50_ms']:.0f} ms",
        True)

    row("Latency p95",
        f"{summary['latency_p95_ms']:.0f} ms",
        not gate_result["latency_failed"])

    row("Avg Cost / Query",
        f"${summary['avg_cost_per_query_usd']:.6f}",
        True)

    row("Total Cost",
        f"${summary['total_cost_usd']:.4f}",
        True)

    print("\n" + "─" * W)
    if gate_result["passed"]:
        print("\n  GATE: PASSED — safe to merge")
    else:
        print("\n  GATE: FAILED — merge blocked")
        if gate_result["hallucination_failed"]:
            print("    ✗ Hallucination rate too high")
        if gate_result["relevancy_failed"]:
            print("    ✗ Relevancy score too low")
        if gate_result["faithfulness_failed"]:
            print("    ✗ Faithfulness score too low")
        if gate_result["latency_failed"]:
            print("    ✗ p95 latency exceeded SLA")
    print("═" * W + "\n")
