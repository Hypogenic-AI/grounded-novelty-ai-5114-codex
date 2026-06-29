# Outline

## Title
- Main claim: prompt-level grounding increases visible literature connection but does not improve judged quality.

## Abstract
- Problem: LLM scientific ideas need novelty and feasibility.
- Approach: 12 AI Idea Bench 2025 contexts, 7 prompt conditions, 84 generated ideas, independent LLM judge.
- Result: no significant judged quality effects; strong prior-work overlap effect.
- Significance: prompt grounding alone is insufficient.

## Introduction
- Hook: fluent ideas can look grounded without being better.
- Gap: prior systems use grounding, but prompt operations are not isolated under matched settings.
- Approach: compare six grounding operations against ungrounded baseline.
- Preview: literature comparison overall 4.00 vs 3.92; no significant quality effects; overlap p=1.06e-9.
- Contributions: matched comparison, independent judging, automatic metrics, design implications.

## Related Work
- Literature-grounded idea generation systems.
- Evaluation of novelty and idea quality.
- Idea generation benchmarks.
- Execution-based scientific agents.

## Methodology
- Matched context-condition setup.
- AI Idea Bench 2025 sample and hidden target fields.
- Prompt conditions.
- Models, temperatures, saved outputs.
- Judged and automatic metrics.
- Paired statistical analysis.

## Results
- Main score table.
- Figures for condition scores, overlap/diversity, novelty-feasibility product.
- Omnibus and pairwise findings.
- Ablation interpretation and qualitative error patterns.

## Discussion and Conclusion
- Grounding changed lexical relation more than quality.
- Shallow audits are weak evidence.
- Limitations: small sample, LLM judge, title-only grounding, no execution.
- Future work: full-text retrieval, anti-copying, diversity, human calibration, execution feedback.
