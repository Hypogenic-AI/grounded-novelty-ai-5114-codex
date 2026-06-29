# Planning: Scientific Idea Generation with Grounded Novelty

## Motivation & Novelty Assessment

### Why This Research Matters
Scientific idea generation is useful only if ideas are both different from prior work and realistic enough to execute. Recent studies show that LLMs can score well on novelty but often lose feasibility, diversity, or execution quality, so researchers need lightweight ways to ground novelty rather than merely request "novel ideas."

### Gap in Existing Work
The gathered literature emphasizes retrieval-grounded systems such as SciMON, ResearchAgent, SciPIP, Chain-of-Ideas, AI-Researcher, and AI Scientist. What is still under-tested is a direct, controlled comparison of multiple grounding styles, using the same topics and model, to see whether deduction, induction, proposal writing, outcome imagination, small empirical audits, and explicit literature comparison improve the novelty-feasibility tradeoff over an ungrounded novelty prompt.

### Our Novel Contribution
This study isolates six grounding operations as prompt-level interventions and compares them against an ungrounded baseline on identical AI research contexts. It combines real LLM generation, independent LLM judging, literature-overlap heuristics, diversity metrics, and paired statistical tests to provide a compact empirical estimate of which grounding operations help.

### Experiment Justification
- Experiment 1: Generate ideas under ungrounded and grounded prompts to directly test whether grounding changes idea quality.
- Experiment 2: Evaluate all ideas with an independent judge model and automatic overlap/diversity metrics to avoid relying only on generator self-assessment.
- Experiment 3: Run paired statistical tests across matched topics to estimate whether observed gains over baseline are larger than prompt/sample noise.
- Experiment 4: Analyze failures qualitatively to identify whether grounding helps novelty, feasibility, specificity, or only presentation quality.

## Research Question
Do LLM-generated scientific ideas improve when novelty is grounded through explicit reasoning operations or evidence, compared with a direct abstract novelty prompt?

## Background and Motivation
The literature review found a shift from unstructured LLM brainstorming toward grounded systems. SciMON and the Idea Novelty Checker use literature comparison, Chain-of-Ideas uses literature trajectories, ResearchAgent uses graph/review feedback, AI-Researcher uses retrieval and proposal ranking, and AI Scientist adds execution. Evaluation remains difficult: human studies report high LLM novelty but weaker feasibility and diversity, while RINoBench and NovBench show that LLM novelty judgments can be poorly calibrated.

## Hypothesis Decomposition
- H1: Grounded prompts increase judged novelty relative to an ungrounded novelty prompt.
- H2: Grounded prompts increase feasibility and specificity, or at least avoid the novelty-feasibility tradeoff.
- H3: Grounded prompts reduce lexical overlap with provided prior-work titles, indicating less direct recombination.
- H4: Different grounding styles produce different benefits: literature comparison should reduce prior-work overlap, proposal writing should improve specificity, and small empirical audits should improve feasibility.

Independent variable: prompt condition.  
Dependent variables: judged novelty, feasibility, specificity, grounding quality, overall score, novelty-feasibility product, prior-work overlap, and within-condition diversity.  
Primary success criterion: at least one grounded condition has a statistically and practically meaningful paired improvement over baseline on overall score and novelty-feasibility product.

## Proposed Methodology

### Approach
Use the local AI Idea Bench 2025 metadata as AI research contexts. For each sampled context, hide the target-paper method and expose only the broad revised topic, keywords, and top cited prior-work titles. Generate one idea per context per condition with `openai/gpt-4.1-mini` through OpenRouter. Judge each generated idea with `google/gemini-2.5-flash`, using a fixed rubric adapted from AI-Researcher and RINoBench: novelty, feasibility, specificity, grounding, risk awareness, and overall quality.

### Experimental Steps
1. Load and validate local datasets, especially AI Idea Bench 2025, RINoBench, and AI-Researcher review data.
2. Sample 12 AI idea contexts with a fixed seed and extract topic, keywords, and top prior-work titles.
3. Compute a small empirical audit for each context: prior-work title term frequencies, repeated terms, missing evaluation cues, and simple lexical novelty opportunities.
4. Generate ideas under seven conditions: ungrounded baseline, deduction, induction, proposal writing, outcome imagination, small experiment, and literature comparison.
5. Evaluate generated ideas with an independent judge model and parse strict JSON scores.
6. Compute automatic metrics: n-gram prior-work overlap, title similarity proxy, word count, JSON parse validity, and TF-IDF diversity within each condition.
7. Run descriptive statistics, Friedman tests across conditions, Wilcoxon signed-rank tests versus baseline with Holm correction, bootstrap confidence intervals, and effect sizes.
8. Inspect representative successes/failures from each condition and write the final report.

### Baselines
Primary baseline: direct ungrounded prompt asking for a novel AI research idea from the broad topic only.  
Reference baselines from literature: AI-Researcher human review scores and RINoBench novelty score distributions are used for context, not direct benchmarking, because this experiment generates new ideas rather than judging existing gold-labeled ideas.

### Evaluation Metrics
- Novelty: judge score 1-5 for conceptual distance from prior work.
- Feasibility: judge score 1-5 for executable study design and plausible resources.
- Specificity: judge score 1-5 for concrete method, data, metrics, and baselines.
- Grounding: judge score 1-5 for using evidence or constraints without copying prior work.
- Overall: judge score 1-5 for scientific promise.
- Composite: novelty-feasibility product and mean of novelty, feasibility, specificity, grounding, and overall.
- Automatic overlap: fraction of generated idea terms overlapping prior-work titles.
- Diversity: average pairwise TF-IDF cosine distance within a condition.

### Statistical Analysis Plan
Use matched-topic comparisons because every topic receives all prompt conditions. Report means, standard deviations, medians, and 95% bootstrap confidence intervals. Use Friedman tests for omnibus condition effects, Wilcoxon signed-rank tests for each grounded condition versus baseline, Holm correction for multiple comparisons, and paired Cohen's d for effect size. Significance level is 0.05, but practical interpretation will emphasize effect size and consistency because n=12 is intentionally compact.

## Expected Outcomes
Support for the hypothesis would look like grounded conditions improving overall quality or novelty-feasibility product without increasing prior-work copying. Refutation would look like no grounded condition outperforming baseline, or improvements occurring only in verbosity/specificity while novelty or feasibility stagnates.

## Timeline and Milestones
- Setup and validation: 10-20 minutes.
- Script implementation: 45-60 minutes.
- API experiment run: 20-60 minutes depending on rate limits.
- Analysis and figures: 20-30 minutes.
- Final documentation and validation: 20-30 minutes.

## Potential Challenges
- API/model variability: record model IDs, timestamps, temperature, prompts, raw outputs, and token usage.
- Judge bias: use a different model family for judging and include automatic overlap/diversity metrics.
- Small sample size: use paired tests and report uncertainty; treat results as preliminary.
- Data leakage from target-paper summaries: do not include target paper names, target methods, or target-paper motivation in prompts.
- JSON parsing failures: retry with strict JSON repair and record failures.
- Rate limits: cache every response and resume incomplete runs.

## Success Criteria
The session succeeds if it produces reproducible scripts, raw model outputs, parsed evaluations, statistical summaries, figures, and a final `REPORT.md` that gives an evidence-backed answer to the research question with limitations clearly stated.
