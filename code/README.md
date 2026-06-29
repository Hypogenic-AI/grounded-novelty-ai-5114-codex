# Cloned Repositories

All repositories were cloned with `--depth 1` under `code/`. They are ignored by `code/.gitignore` but available locally for experimentation.

| Name | URL | Location | Purpose | Notes |
|---|---|---|---|---|
| SciMON / CLBD | https://github.com/eaglew/clbd | `code/scimon_clbd/` | Literature-grounded idea generation optimized for novelty | Large clone (~587 MB); requires separate NLP/biochemical conda envs and PyTorch. |
| ResearchAgent | https://github.com/JinheonBaek/ResearchAgent | `code/researchagent/` | Generates problems, methods, experiment designs from Semantic Scholar paper IDs and knowledge store | Needs OpenAI key and Semantic Scholar access. Entry: `code/researchagent/code/main.py`. |
| SciPIP | https://github.com/cheerss/scipip | `code/scipip/` | Scientific paper idea proposer with Neo4j literature database | Requires Neo4j, LLM API config, and external literature DB download. Entry: `app.py` or `src/generator.py`. |
| CoI-Agent | https://github.com/DAMO-NLP-SG/CoI-Agent | `code/coi_agent/` | Chain-of-Ideas agent and Idea Arena evaluation | Requires GROBID/SciPDF Parser, Semantic Scholar API, OpenAI-compatible API. Entry: `main.py`. |
| AI-Researcher | https://github.com/NoviScl/AI-Researcher | `code/ai_researcher_human_study/` | Ideation agent and human/execution review data from large-scale study | Data copied to `datasets/ai_researcher_human_study/`; pipeline needs OpenAI/Anthropic/S2 keys. |
| AI Scientist | https://github.com/SakanaAI/AI-Scientist | `code/ai_scientist/` | End-to-end ideation, code execution, paper writing, and review | GPU and LaTeX recommended; API keys needed. Entry: `launch_scientist.py`. |
| RINoBench | https://github.com/TimSchopf/RINoBench | `code/rinobench/` | Research idea novelty judgment benchmark code | Dataset downloaded to `datasets/rinobench/`. |
| Idea Novelty Checker | https://github.com/simra-shahid/idea_novelty_checker | `code/idea_novelty_checker/` | RAG novelty checker with retrieval/reranking/facet comparison | Needs OpenAI or Anthropic plus S2 key; GPU recommended for SPECTER2 reranking. Entry: `main.py`. |
| IdeaBench | https://github.com/amir-hassan25/IdeaBench | `code/ideabench/` | Research idea generation benchmark and Insight Score pipeline | Data copied to `datasets/ideabench/`; API keys required for generation/evaluation. |
| AI Idea Bench 2025 | https://github.com/yansheng-qiu/AI_Idea_Bench_2025 | `code/ai_idea_bench_2025/` | AI research idea-generation benchmark and evaluation scripts | Requires GROBID/SciPDF Parser and multiple APIs; HF metadata downloaded to `datasets/ai_idea_bench_2025/`. |
| DiscoveryBench | https://github.com/allenai/discoverybench | `code/discoverybench/` | Data-driven discovery benchmark and agent/eval scripts | Answer keys copied to `datasets/discoverybench/`; entries `discovery_agent.py`, `discovery_eval.py`. |
| ScienceAgentBench | https://github.com/OSU-NLP-Group/ScienceAgentBench | `code/scienceagentbench/` | Scientific coding-task benchmark and evaluation harness | HF annotations downloaded; full benchmark requires author-provided archive/password. |
| MLAgentBench | https://github.com/snap-stanford/mlagentbench | `code/mlagentbench/` | Executable ML experimentation tasks for language agents | Setup via `pip install -e .`; Kaggle tasks need Kaggle API; entry `MLAgentBench.runner`. |
| LiveIdeaBench | https://github.com/x66ccff/liveideabench | `code/liveideabench/` | Minimal-context scientific creativity evaluation | Full HF CSV is 1.14 GB; local sample only. Entry: `run.py`. |

## Quick Recommendations

- For a first experiment, use the local datasets and implement a simple generator/evaluator rather than installing full SciPIP/CoI/AI-Scientist stacks.
- Most repo pipelines require external API keys; plan a no-API baseline using local datasets first.
- Best reusable evaluation code candidates: `code/rinobench/`, `code/idea_novelty_checker/`, `code/ideabench/`, `code/discoverybench/`.
- Best reusable generation patterns: SciMON novelty boosting, ResearchAgent reviewer feedback, CoI-Agent literature chains, AI-Researcher proposal pipeline.
