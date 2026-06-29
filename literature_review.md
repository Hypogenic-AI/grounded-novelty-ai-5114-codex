# Literature Review: Scientific Idea Generation with Grounded Novelty

## Review Scope

### Research Question

Can LLMs generate better scientific ideas when novelty is grounded through literature comparison, structured reasoning, proposal writing, imagined outcomes, small experiments, or data-driven evidence rather than abstract novelty prompting?

### Inclusion Criteria

- LLM or agent systems for scientific idea, hypothesis, or research-proposal generation.
- Work that explicitly grounds generation/evaluation in literature, knowledge graphs, datasets, experiments, or expert review.
- Benchmarks or datasets useful for evaluating novelty, feasibility, idea quality, or scientific execution.
- Recent AI/NLP/scientific-discovery papers, with emphasis on 2023-2026.

### Exclusion Criteria

- General creativity or brainstorming papers without scientific grounding/evaluation.
- Pure literature-review systems that do not generate or evaluate research ideas.
- Closed resources without accessible paper, code, or usable metadata.

### Search Log

| Date | Query/Source | Result |
|---|---|---|
| 2026-06-29 | local paper-finder script | Timed out/no output; switched to manual/API search. |
| 2026-06-29 | web/arXiv/Semantic Scholar: "scientific idea generation large language models novelty" | Found SciMON, ResearchAgent, SciPIP, human LLM idea study. |
| 2026-06-29 | web/arXiv/GitHub: "grounded novelty scientific idea generation LLM" | Found RINoBench, Literature-Grounded Novelty Assessment, IdeaBench, AI Idea Bench 2025. |
| 2026-06-29 | web/GitHub/HF: "data-driven discovery agent benchmark" | Found MLAgentBench, DiscoveryBench, ScienceAgentBench. |

## Research Area Overview

The field has moved from unstructured LLM brainstorming toward systems that expose models to scientific evidence and force some comparison with prior work. The strongest pattern is retrieval grounding: SciMON retrieves inspirations and iteratively asks the model to revise ideas that overlap with prior work; ResearchAgent retrieves references/entities around a core paper and revises with reviewing agents; SciPIP improves retrieval with semantic, citation, and full-text information; Chain-of-Ideas organizes papers into developmental chains so the model sees how a domain evolved.

Evaluation is the bottleneck. The large Stanford human study shows LLM ideas can be judged more novel than expert ideas under controlled conditions, but also finds weaker feasibility, poor diversity under scaling, and unreliable LLM self-evaluation. RINoBench and NovBench show that novelty judgment itself is hard: LLM rationales may resemble expert rationales while their numeric novelty scores still diverge from human gold labels. The practical implication is that any grounded-novelty experiment should evaluate multiple axes: novelty, feasibility, specificity, diversity, literature overlap, and, where possible, execution outcomes.

## Key Papers

### SciMON: Scientific Inspiration Machines Optimized for Novelty

- **Authors**: Wang, Downey, Ji, Hope
- **Year**: 2023/2024
- **Source**: arXiv / ACL 2024
- **Key contribution**: Natural-language scientific idea generation grounded in literature inspirations and explicit novelty boosting.
- **Methodology**: Extracts background contexts and target ideas from scientific papers, retrieves inspiration papers/knowledge, generates ideas, then iteratively compares generated ideas to prior literature and revises until overlap drops below a threshold.
- **Datasets used**: ACL Anthology-derived AI/NLP dataset with temporal split; gold test subset of 194 instances; biomedical transfer experiments.
- **Results**: GPT-4 few-shot variants are stronger than T5/GPT-3.5 baselines, but outputs still often lack novelty/technical depth; grounding and iterative novelty boosting partially mitigate this.
- **Code available**: `code/scimon_clbd/`, https://github.com/eaglew/clbd
- **Relevance**: Directly tests the hypothesis that novelty improves when grounded by literature comparison.

### ResearchAgent

- **Authors**: Baek, Jauhar, Cucerzan, Hwang
- **Year**: 2024/2025
- **Source**: arXiv / NAACL 2025
- **Key contribution**: Iterative generation of problems, methods, and experiment designs from a core paper plus scientific graph/entity context.
- **Methodology**: Uses Semantic Scholar paper IDs, references, and entity-centric knowledge stores; reviewing agents score ideas on criteria such as originality, feasibility, validity, rigor, generalizability, robustness, and reproducibility.
- **Datasets used**: 300 post-May-2023 high-impact core papers sampled from Semantic Scholar Academic Graph.
- **Results**: Full ResearchAgent outperforms ablated variants in human and model-based evaluation.
- **Code available**: `code/researchagent/`, https://github.com/JinheonBaek/ResearchAgent
- **Relevance**: Strong baseline for literature- and review-grounded proposal generation.

### SciPIP

- **Authors**: Wang et al.
- **Year**: 2024/2025
- **Source**: arXiv / OpenReview
- **Key contribution**: Scientific Paper Idea Proposer with improved literature retrieval and dual-path generation.
- **Methodology**: Builds a literature DB with keyword, semantic, citation, and full-text information; retrieves at multiple granularity levels; generates ideas from both retrieved content and LLM internal knowledge.
- **Datasets used**: Literature database covering AI areas such as NLP/CV/ML; external Neo4j data download.
- **Results**: Reports improved novelty, feasibility, and practical value across domains.
- **Code available**: `code/scipip/`, https://github.com/cheerss/scipip
- **Relevance**: Useful implementation pattern for full-text literature grounding.

### Chain of Ideas

- **Authors**: Li et al.
- **Year**: 2024/2025
- **Source**: arXiv / EMNLP Findings 2025
- **Key contribution**: Organizes literature into backward/forward chains to mirror progressive research development.
- **Methodology**: Retrieves anchor papers, constructs multiple idea chains from references and subsequent work, predicts future trends, generates ideas/experiment designs, then applies novelty-checking refinement.
- **Datasets used**: AI-domain idea-generation evaluation.
- **Results**: CoI-Agent ranks first among automated baselines in Idea Arena and is reported comparable to human ideas on novelty.
- **Code available**: `code/coi_agent/`, https://github.com/DAMO-NLP-SG/CoI-Agent
- **Relevance**: Operationalizes "induction from literature trajectories" as a grounded novelty method.

### Can LLMs Generate Novel Research Ideas?

- **Authors**: Si, Yang, Hashimoto
- **Year**: 2024
- **Source**: arXiv
- **Key contribution**: Large-scale controlled human study comparing expert NLP researchers and an LLM ideation agent.
- **Methodology**: 100+ NLP researchers generated/reviewed ideas; blind reviews scored novelty, excitement, feasibility, effectiveness, and overall quality. LLM agent used retrieval augmentation, overgeneration, and reranking.
- **Datasets used**: Seven prompting-based NLP topics; released review scores/data in AI-Researcher repo.
- **Results**: LLM ideas were judged significantly more novel than human expert ideas (p < 0.05), slightly weaker on feasibility; LLM self-evaluation and generation diversity were failure points.
- **Code/data available**: `code/ai_researcher_human_study/`, `datasets/ai_researcher_human_study/`, https://github.com/NoviScl/AI-Researcher
- **Relevance**: Best human-evaluation evidence for the core claim; also warns that novelty without feasibility/diversity is insufficient.

### The AI Scientist

- **Authors**: Lu et al.
- **Year**: 2024
- **Source**: arXiv; Nature version appeared in 2026
- **Key contribution**: End-to-end automated scientific discovery pipeline.
- **Methodology**: Generates ideas, writes code, executes experiments, plots results, writes papers, and performs simulated review; includes Semantic Scholar novelty checking.
- **Datasets/tasks used**: ML templates in diffusion modeling, transformer language modeling, and grokking/learning dynamics.
- **Results**: Produces complete workshop-style papers at low API cost, but novelty checking has known limitations and downstream execution quality varies.
- **Code available**: `code/ai_scientist/`, https://github.com/SakanaAI/AI-Scientist
- **Relevance**: Baseline for proposal writing plus small-experiment grounding.

### RINoBench

- **Authors**: Schopf, Farber
- **Year**: 2026
- **Source**: arXiv / LREC 2026
- **Key contribution**: Benchmark for research idea novelty judgment.
- **Methodology**: Converts ICLR 2022/2023 review data into 1,381 research ideas with expert-derived novelty scores, justifications, and related works.
- **Metrics**: novelty score classification/MAE plus text-justification metrics.
- **Results**: LLM-generated rationales align with human rationales more than their novelty scores align with human labels; reasoning models help but remain unreliable.
- **Code/data available**: `code/rinobench/`, `datasets/rinobench/`, https://github.com/TimSchopf/RINoBench
- **Relevance**: Recommended primary automated benchmark for novelty-judgment calibration.

### Literature-Grounded Novelty Assessment

- **Authors**: Shahid et al.
- **Year**: 2025
- **Source**: arXiv / ACL SDP
- **Key contribution**: Idea Novelty Checker, a retrieve-then-rerank RAG framework for novelty assessment.
- **Methodology**: Combines keyword/snippet retrieval, embedding filtering, facet-based LLM reranking, and expert-labeled examples. Facets include purpose, mechanism, evaluation, and application domain.
- **Datasets used**: 67 consensus-labeled examples, split into 35 train and 32 test examples.
- **Results**: About 13% higher agreement than existing approaches; ablations show facet reranking is important.
- **Code available**: `code/idea_novelty_checker/`, https://github.com/simra-shahid/idea_novelty_checker
- **Relevance**: Directly supports literature-comparison evaluation of grounded novelty.

### IdeaBench and AI Idea Bench 2025

- **Authors**: Guo et al.; Qiu et al.
- **Years**: 2024; 2025
- **Sources**: arXiv and GitHub/Hugging Face
- **Key contributions**: Datasets and evaluation frameworks for generating research ideas from paper/reference contexts.
- **Methodology**: Compare generated ideas to target paper ideas and evaluate quality with LLM-assisted ranking/Insight Scores or reference-based matching.
- **Datasets used**: IdeaBench has 2,374 target papers and 29,408 references; AI Idea Bench 2025 has 3,495 AI papers and motivating papers.
- **Code/data available**: `datasets/ideabench/`, `datasets/ai_idea_bench_2025/`, `code/ideabench/`, `code/ai_idea_bench_2025/`
- **Relevance**: Good input-output structure for testing whether grounded prompts recover plausible research directions.

### LiveIdeaBench and NovBench

- **Authors**: Ruan et al.; Wu et al.
- **Years**: 2024/2026; 2026
- **Key contributions**: LiveIdeaBench evaluates divergent scientific idea generation from minimal keyword prompts; NovBench evaluates academic paper novelty assessment text.
- **Methodology**: LiveIdeaBench scores originality, feasibility, fluency, flexibility, and clarity across 1,180 keywords and 22 domains. NovBench uses 1,684 paper-review pairs and evaluates relevance, correctness, coverage, clarity.
- **Data/code available**: `datasets/liveideabench_sample/`, `code/liveideabench/`; NovBench data was not found as a direct public download during this pass.
- **Relevance**: LiveIdeaBench is a useful ungrounded/minimal-context contrast; NovBench supports paper-level novelty critique framing.

### MLAgentBench, DiscoveryBench, and ScienceAgentBench

- **Authors**: Huang et al.; Majumder et al.; Chen et al.
- **Years**: 2023/2024; 2024/2025; 2024/2025
- **Key contributions**: Benchmarks for executable ML experimentation and data-driven scientific discovery.
- **Methodology**: Agents operate on task workspaces/datasets, write code, run experiments, and are evaluated by task-specific metrics or generated programs.
- **Results**: MLAgentBench reports best average success around 37.5%; DiscoveryBench best system peaks around 25%; ScienceAgentBench best agents solve only about one-third to 42.2% depending on model/compute.
- **Code/data available**: `code/mlagentbench/`, `code/discoverybench/`, `code/scienceagentbench/`, plus local annotation/answer-key data.
- **Relevance**: Best resources for testing "small experiments" and "outcome imagination vs actual execution" as grounding mechanisms.

### KG-CoI Hypothesis Generation

- **Authors**: Xiong et al.
- **Year**: 2024
- **Key contribution**: Knowledge Grounded Chain of Ideas for hypothesis generation.
- **Methodology**: Integrates external knowledge graphs into a chain-of-ideas reasoning process and detects hallucinations with KG support.
- **Results**: Reports improved hypothesis accuracy and reduced hallucination.
- **Code availability**: no standalone repo found in this pass; related authors also maintain IdeaBench.
- **Relevance**: Structured knowledge grounding is a useful alternative to pure literature retrieval.

## Common Methodologies

- **Ungrounded prompting**: Ask an LLM for novel ideas from a topic. This is the main baseline and should be expected to overclaim novelty.
- **Retrieval-grounded generation**: Retrieve papers, abstracts, snippets, citations, or full text before generation. Used by SciMON, ResearchAgent, SciPIP, AI-Researcher, AI Scientist.
- **Iterative novelty checking**: Generate an idea, compare to prior work, revise if overlap is found. Used by SciMON, CoI-Agent, AI Scientist, Idea Novelty Checker.
- **Literature trajectory induction**: Organize references and citing papers into chains or graph neighborhoods to infer trends. Used by Chain-of-Ideas and ResearchAgent.
- **Proposal writing**: Expand ideas into motivation, method, baseline, dataset, and experiment plan. Used by AI-Researcher, ResearchAgent, CoI-Agent, AI Scientist.
- **Experiment execution**: Run small computational experiments and judge outcomes. Used by AI Scientist and the MLAgentBench/DiscoveryBench/ScienceAgentBench family.
- **LLM-as-judge with calibration**: Common but risky. RINoBench and NovBench show it must be calibrated against human labels.

## Standard Baselines

- Direct topic-to-idea prompt with no retrieval.
- Topic plus retrieved abstracts/references.
- Topic plus full-text snippets or paper facets.
- ResearchAgent without entity retrieval; ResearchAgent full.
- CoI-Agent vs direct literature aggregation vs naive prompting.
- AI Scientist novelty check vs Idea Novelty Checker.
- Human expert ideas where available from AI-Researcher.
- ReAct/CodeAct/self-debug agents on executable benchmarks.

## Evaluation Metrics

- **Novelty**: expert novelty score, binary novel/not novel, pairwise novelty ranking, RINoBench novelty-score error.
- **Feasibility**: expert or LLM-judge score; explicit baseline/dataset/compute plausibility checks.
- **Specificity/technical depth**: method clarity, evaluation design detail, baseline coverage.
- **Diversity**: semantic clustering, self-BLEU, distinct-n, duplicate rate.
- **Grounding quality**: citation/retrieval relevance, overlap with prior papers, facet coverage.
- **Proposal quality**: clarity, significance, reproducibility, robustness, validity.
- **Execution outcome**: task success, metric improvement, generated-code pass rate, cost/tokens/runtime.

## Datasets in the Literature

- **RINoBench**: novelty judgment labels and related works for 1,381 ideas.
- **AI-Researcher human study data**: expert reviews of human/AI/AI+reranked ideas and execution-study records.
- **IdeaBench**: target papers and references across eight domains.
- **AI Idea Bench 2025**: 3,495 AI papers with motivating papers and ground-truth target content.
- **LiveIdeaBench**: large minimal-context scientific creativity benchmark; only partial local sample due size.
- **ScienceAgentBench**: 102 scientific coding tasks; local annotation sheet downloaded.
- **DiscoveryBench**: answer keys and code for data-driven discovery; local answer keys copied.

## Gaps and Opportunities

- **Novelty is not enough**: high judged novelty can trade off against feasibility and specificity.
- **LLM self-evaluation is unreliable**: multiple papers report mismatch between LLM judgments and human labels.
- **Diversity collapses under scaling**: overgeneration may produce duplicates unless diversity is explicitly optimized.
- **Grounding quality is uneven**: keyword retrieval misses relevant work; full-text retrieval and reranking help but add infrastructure cost.
- **Execution is underused in ideation studies**: most papers judge ideas as text; few test whether ideas survive implementation.
- **Data contamination is hard**: benchmarks using known papers must use temporal splits or recent post-cutoff papers.

## Recommendations for Our Experiment

- **Primary datasets**: RINoBench for novelty judgment; AI-Researcher review data for human-vs-AI idea quality; IdeaBench/AI Idea Bench 2025 for idea-generation prompts; ScienceAgentBench or DiscoveryBench for small-experiment grounding.
- **Core baselines**: ungrounded prompt; retrieved abstracts; retrieved abstracts plus explicit novelty comparison; CoI-style literature chain; proposal-writing prompt; outcome-imagination prompt; small-experiment agent.
- **Metrics**: novelty score, feasibility score, related-work overlap, diversity, proposal completeness, and execution success where applicable.
- **Design caution**: do not rely on one LLM judge. Use at least one benchmark with gold novelty labels and a separate judge prompt for feasibility/specificity.
- **Most practical first experiment**: Take RINoBench or IdeaBench prompts, generate ideas under several grounding conditions, then evaluate with RINoBench-style novelty scoring plus feasibility/proposal rubrics.
