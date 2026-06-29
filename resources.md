# Resources Catalog

## Summary

Resources gathered for **Scientific Idea Generation with Grounded Novelty**.

- Papers downloaded: 16
- Dataset folders prepared: 7
- Repositories cloned: 14
- Environment: local `.venv` created with `uv`; dependencies tracked in `pyproject.toml`

## Papers

| Title | Year | File | Key Info |
|---|---:|---|---|
| Can LLMs Generate Novel Research Ideas? | 2024 | `papers/2409.04109_llm_research_ideas_human_study.pdf` | Human-vs-LLM expert ideation study |
| SciMON | 2023/2024 | `papers/2305.14259_scimon.pdf` | Literature-grounded novelty boosting |
| ResearchAgent | 2024/2025 | `papers/2404.07738_researchagent.pdf` | Graph/entity-grounded idea refinement |
| SciPIP | 2024/2025 | `papers/2410.23166_scipip.pdf` | Full-text/citation-aware idea proposer |
| Chain of Ideas | 2024/2025 | `papers/2410.13185_chain_of_ideas.pdf` | Literature-chain induction and Idea Arena |
| The AI Scientist | 2024 | `papers/2408.06292_ai_scientist.pdf` | End-to-end automated research pipeline |
| RINoBench | 2026 | `papers/2603.10303_rinobench.pdf` | Novelty judgment benchmark |
| Literature-Grounded Novelty Assessment | 2025 | `papers/2506.22026_literature_grounded_novelty_assessment.pdf` | RAG novelty checker |
| IdeaBench | 2024 | `papers/2411.02429_ideabench.pdf` | Idea generation benchmark and Insight Score |
| AI Idea Bench 2025 | 2025 | `papers/2504.14191_ai_idea_bench_2025.pdf` | AI target/motivating paper benchmark |
| LiveIdeaBench | 2024/2026 | `papers/2412.17596_liveideabench.pdf` | Minimal-context creativity benchmark |
| NovBench | 2026 | `papers/2604.11543_novbench.pdf` | Paper novelty assessment benchmark |
| MLAgentBench | 2023/2024 | `papers/2310.03302_mlagentbench.pdf` | ML experimentation benchmark |
| DiscoveryBench | 2024/2025 | `papers/2407.01725_discoverybench.pdf` | Data-driven discovery benchmark |
| ScienceAgentBench | 2024/2025 | `papers/2410.05080_scienceagentbench.pdf` | Scientific coding-task benchmark |
| KG-CoI Hypothesis Generation | 2024 | `papers/2411.02382_kg_coi_hypothesis_generation.pdf` | Knowledge-graph-grounded hypothesis chains |

See `papers/README.md` for details.

## Datasets

| Name | Source | Size | Location | Notes |
|---|---|---:|---|---|
| RINoBench | Hugging Face | 1,104 train / 277 test | `datasets/rinobench/` | Novelty labels, reasoning, related works |
| AI Idea Bench 2025 | Hugging Face | 3,495 rows | `datasets/ai_idea_bench_2025/` | Full 30 GB zip skipped; metadata downloaded |
| ScienceAgentBench annotations | Hugging Face | 102 tasks | `datasets/scienceagentbench/` | Full benchmark requires external archive |
| LiveIdeaBench v2 sample | Hugging Face | 200 KB sample | `datasets/liveideabench_sample/` | Full CSV is 1.14 GB |
| IdeaBench | GitHub clone | 2,374 targets / 23,460 refs | `datasets/ideabench/` | Copied from cloned repo |
| AI-Researcher review data | GitHub clone | 20 ideation / 23 execution records | `datasets/ai_researcher_human_study/` | Human/expert review data |
| DiscoveryBench answer keys | GitHub clone | 239 real / 200 synthetic | `datasets/discoverybench/` | Answer keys only |

See `datasets/README.md` and `datasets/dataset_summary.json`.

## Code Repositories

| Name | URL | Location | Purpose |
|---|---|---|---|
| SciMON / CLBD | https://github.com/eaglew/clbd | `code/scimon_clbd/` | Novelty-optimized literature-grounded generation |
| ResearchAgent | https://github.com/JinheonBaek/ResearchAgent | `code/researchagent/` | Graph/entity-grounded ideation |
| SciPIP | https://github.com/cheerss/scipip | `code/scipip/` | Paper idea proposer with literature DB |
| CoI-Agent | https://github.com/DAMO-NLP-SG/CoI-Agent | `code/coi_agent/` | Chain-of-Ideas generation |
| AI-Researcher | https://github.com/NoviScl/AI-Researcher | `code/ai_researcher_human_study/` | Ideation agent and human-study data |
| AI Scientist | https://github.com/SakanaAI/AI-Scientist | `code/ai_scientist/` | End-to-end automated research |
| RINoBench | https://github.com/TimSchopf/RINoBench | `code/rinobench/` | Novelty judgment benchmark |
| Idea Novelty Checker | https://github.com/simra-shahid/idea_novelty_checker | `code/idea_novelty_checker/` | Literature-grounded novelty assessment |
| IdeaBench | https://github.com/amir-hassan25/IdeaBench | `code/ideabench/` | Idea-generation benchmark |
| AI Idea Bench 2025 | https://github.com/yansheng-qiu/AI_Idea_Bench_2025 | `code/ai_idea_bench_2025/` | AI idea benchmark scripts |
| DiscoveryBench | https://github.com/allenai/discoverybench | `code/discoverybench/` | Data-driven discovery benchmark |
| ScienceAgentBench | https://github.com/OSU-NLP-Group/ScienceAgentBench | `code/scienceagentbench/` | Scientific coding benchmark |
| MLAgentBench | https://github.com/snap-stanford/mlagentbench | `code/mlagentbench/` | ML experimentation benchmark |
| LiveIdeaBench | https://github.com/x66ccff/liveideabench | `code/liveideabench/` | Minimal-context creativity evaluation |

See `code/README.md` for setup notes and blockers.

## Search Strategy

The local paper-finder script was attempted first but stalled without output, so resource gathering used manual searches across arXiv, Semantic Scholar snippets, GitHub, Papers with Code-style repository links, Hugging Face datasets, and paper README/source links.

Search concepts included:

- scientific idea generation LLM novelty
- literature-grounded novelty assessment scientific ideas
- research idea generation benchmark dataset
- automated scientific discovery agent benchmark
- data-driven discovery with LLM agents

## Selection Criteria

- Direct relevance to scientific idea/hypothesis generation or novelty judgment.
- Grounding mechanism is explicit: retrieval, literature chains, knowledge graphs, proposal writing, or executable experiments.
- Dataset/code is public or partially accessible.
- Useful downstream evaluation signal, not only demo software.

## Challenges and Workarounds

- Paper-finder service timed out. Manual web/API search was used.
- LiveIdeaBench v2 full CSV is about 1.14 GB and HF viewer reports a parsing issue. Only a 200 KB sample and README were saved.
- AI Idea Bench 2025 has a 30 GB full zip. The smaller parquet and target JSON metadata were downloaded; the full zip was skipped.
- ScienceAgentBench full benchmark requires a separate password-protected archive. HF annotations were downloaded.
- Many repo pipelines require API keys, GROBID/SciPDF Parser, Neo4j, GPUs, or Docker; these were documented instead of installed globally.

## Recommendations for Experiment Design

1. **Primary datasets**: start with RINoBench and IdeaBench/AI Idea Bench 2025. Add AI-Researcher review data for human-calibrated idea-quality analysis.
2. **Baseline methods**: ungrounded prompt, retrieved-abstract prompt, full literature-comparison prompt, CoI-style chain prompt, proposal-writing prompt, outcome-imagination prompt, and small-experiment agent.
3. **Evaluation metrics**: novelty, feasibility, specificity, diversity, related-work overlap, and execution success for task-based benchmarks.
4. **Code to adapt**: use RINoBench for evaluation format, Idea Novelty Checker for retrieval/facet novelty assessment, AI-Researcher for proposal pipeline prompts, and DiscoveryBench/ScienceAgentBench for execution tasks.

## Research Execution Outputs

The completed experiment used the resources above as follows:

- **Primary generation data**: `datasets/ai_idea_bench_2025/test.parquet`.
- **Rubric and design context**: `literature_review.md`, RINoBench, AI-Researcher review data, and the prompt patterns documented in the cloned repositories.
- **Experiment plan**: `planning.md`.
- **Execution code**: `src/run_grounded_ideation_experiment.py`.
- **Analysis code**: `src/analyze_grounded_ideation.py`.
- **Raw model outputs**: `results/model_outputs/generations.jsonl` and `results/model_outputs/evaluations.jsonl`.
- **Analysis tables**: `results/tables/condition_summary.csv`, `results/tables/omnibus_tests.csv`, and `results/tables/pairwise_tests_vs_ungrounded.csv`.
- **Figures**: `figures/condition_scores.png`, `figures/overlap_diversity.png`, and `figures/novelty_feasibility_product.png`.
- **Final report**: `REPORT.md`.

Summary result: in this 12-context pilot, prompt-level grounding did not significantly improve judged idea quality over the ungrounded baseline, but it did significantly increase lexical overlap with prior-work titles.
