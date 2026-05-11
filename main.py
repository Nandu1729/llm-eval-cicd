import sys
from dotenv import load_dotenv
load_dotenv()

from app.evaluator import run_evaluation
from app.dashboard import compute_summary, print_dashboard
from app.gate import evaluate_gate

DIVIDER = "═" * 58


def main():
    print("\n" + DIVIDER)
    print("   LLM Eval CI/CD Pipeline")
    print("   Powered by Groq + LangGraph")
    print(DIVIDER)

    results = run_evaluation()
    summary = compute_summary(results)
    gate_result = evaluate_gate(summary)
    print_dashboard(summary, gate_result)

    if not gate_result["passed"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
