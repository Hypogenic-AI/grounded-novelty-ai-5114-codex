# Grounded Novelty for Scientific Idea Generation

This workspace contains a compact empirical study of whether prompt-level grounding improves LLM scientific idea generation. It compares ungrounded ideation against deduction, induction, proposal writing, outcome imagination, a small metadata audit, and explicit literature comparison.

## Key Findings

- 84 real LLM-generated ideas were produced from 12 AI Idea Bench contexts.
- Grounded prompts did not significantly improve judged novelty, feasibility, overall score, or novelty-feasibility product over the ungrounded baseline.
- Literature comparison had the highest mean overall score (4.00 vs. 3.92 baseline), but the difference was not statistically reliable.
- Grounded prompts significantly increased lexical overlap with prior-work titles, suggesting stronger literature anchoring but also more copying/recombination risk.
- The lightweight small-experiment audit was not enough to improve idea quality.

See `REPORT.md` for full methodology, statistics, figures, and limitations.

## Reproduce

The isolated environment is already configured in `.venv/` and dependencies are tracked in `pyproject.toml`.

```bash
source .venv/bin/activate
python src/run_grounded_ideation_experiment.py --limit 12 --judge-max-tokens 2000 --sleep 0.1
python src/analyze_grounded_ideation.py
```

The experiment requires `OPENROUTER_KEY` or `OPENROUTER_API_KEY` for real model calls. Cached outputs are reused automatically from `results/model_outputs/`, so rerunning does not repeat completed calls.

## File Structure

- `planning.md`: preregistered motivation, design, metrics, and analysis plan.
- `REPORT.md`: final research report with actual results.
- `src/run_grounded_ideation_experiment.py`: sampling, prompt construction, API calls, and response caching.
- `src/analyze_grounded_ideation.py`: metrics, statistical tests, figures, and error analysis.
- `results/model_outputs/`: raw LLM generations and judge responses.
- `results/tables/`: score summaries and statistical tests.
- `results/evaluations/error_analysis.md`: representative best/worst cases by condition.
- `figures/`: generated plots.
- `datasets/`, `papers/`, `code/`: pre-gathered local resources used to design the study.
