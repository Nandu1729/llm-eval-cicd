# LLM Eval CI/CD Pipeline

An automated evaluation pipeline that runs every time someone changes a prompt, swaps a model, or updates a RAG knowledge base — just like unit tests run when code changes. Powered by **Groq + LangChain**.

---

## How It Works

```
git push → GitHub Actions → Run Eval on Golden Dataset → Compute Metrics → Gate Check
                                                                                 ↓
                                                                    PASS → merge allowed
                                                                    FAIL → merge blocked
```

---

## Metrics Measured

| Metric | Description |
|---|---|
| **Hallucination Rate** | % of responses with made-up facts |
| **Answer Relevancy** | % of responses relevant to the question |
| **Faithfulness** | % of responses faithful to expected answer |
| **Latency p50 / p95** | Median and 95th percentile response time |
| **Cost per Query** | Estimated USD cost per LLM call |

---

## Gate Thresholds (configurable in `config.yaml`)

```yaml
thresholds:
  max_hallucination_rate: 0.05    # block if hallucination > 5%
  min_relevancy_score: 0.80       # block if relevancy < 80%
  min_faithfulness_score: 0.75    # block if faithfulness < 75%
  max_p95_latency_ms: 5000        # block if p95 latency > 5s
```

---

## Project Structure

```
llm-eval-cicd/
├── main.py                        # Entry point
├── config.yaml                    # Gate thresholds
├── data/
│   └── golden_dataset.json        # 20 QA pairs (expandable to 100+)
├── .github/
│   └── workflows/
│       └── eval.yml               # GitHub Actions CI
└── app/
    ├── evaluator.py               # Runs all samples
    ├── llm_call.py                # Groq call + latency + cost tracking
    ├── metrics.py                 # LLM judge (hallucination, relevancy, faithfulness)
    ├── gate.py                    # Pass/fail gate logic
    ├── dashboard.py               # Terminal results dashboard
    └── dataset.py                 # Golden dataset loader
```

---

## Setup

```bash
git clone https://github.com/Nandu1729/llm-eval-cicd
cd llm-eval-cicd
pip3 install -r requirements.txt
cp .env.example .env        # Add your GROQ_API_KEY
python3 main.py
```

---

## Example Output

```
  [01/20] What is Python?...
  [02/20] What is a REST API?...
  ...

══════════════════════════════════════════════════════════
   LLM Eval CI/CD  —  Results Dashboard
══════════════════════════════════════════════════════════

  Samples evaluated : 20

  METRIC                           VALUE        STATUS
  ──────────────────────────────────────────────────────
  Hallucination Rate               2.0%         PASS
  Answer Relevancy                 95.0%        PASS
  Faithfulness                     90.0%        PASS
  Latency p50                      820 ms       PASS
  Latency p95                      1340 ms      PASS
  Avg Cost / Query                 $0.000012    PASS
  Total Cost                       $0.0002      PASS

  ──────────────────────────────────────────────────────
  GATE: PASSED — safe to merge
══════════════════════════════════════════════════════════
```

---

## CI/CD — GitHub Actions

On every `git push` or pull request, the pipeline runs automatically and blocks the merge if any metric fails:

```yaml
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
```

Add your `GROQ_API_KEY` under **Settings → Secrets → Actions** in your GitHub repo.

---

## Tech Stack

- [Groq](https://groq.com/) — LLM inference (llama-3.1-8b-instant)
- [LangChain](https://github.com/langchain-ai/langchain) — LLM integration
- [GitHub Actions](https://github.com/features/actions) — CI/CD automation
- [PyYAML](https://pyyaml.org/) — config/threshold management

---

## Related Projects

- [Self-Healing RAG Pipeline](https://github.com/Nandu1729/self-healing-rag)
- [LLM Guardrails Gateway](https://github.com/Nandu1729/llm-guardrails-gateway)
