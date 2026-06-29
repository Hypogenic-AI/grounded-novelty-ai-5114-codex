# Downloaded Datasets

This directory contains local datasets and samples for experiments. Large data files are excluded from git by `datasets/.gitignore`; small sample files and this README are kept for inspection and reproducibility.

## Summary

| Dataset | Source | Local Location | Size/Rows | Task Fit |
|---|---|---:|---|---|
| RINoBench | https://huggingface.co/datasets/TimSchopf/RINoBench | `datasets/rinobench/` | train 1,104; test 277 | Novelty judgment against related works |
| AI Idea Bench 2025 | https://huggingface.co/datasets/yanshengqiu/AI_Idea_Bench_2025 | `datasets/ai_idea_bench_2025/` | 3,495 rows | Idea generation from motivating papers |
| ScienceAgentBench annotations | https://huggingface.co/datasets/osunlp/ScienceAgentBench | `datasets/scienceagentbench/` | 102 tasks | Data-driven scientific coding tasks |
| LiveIdeaBench v2 sample | https://huggingface.co/datasets/6cf/liveideabench-v2 | `datasets/liveideabench_sample/` | first 200 KB sample | Divergent idea generation scoring |
| IdeaBench | https://github.com/amir-hassan25/IdeaBench | `datasets/ideabench/` | 2,374 target papers; 23,460 filtered refs | Research idea generation benchmark |
| AI-Researcher human/execution reviews | https://github.com/NoviScl/AI-Researcher | `datasets/ai_researcher_human_study/` | 20 ideation records; 23 execution records | Human vs AI idea review scores |
| DiscoveryBench answer keys | https://github.com/allenai/discoverybench | `datasets/discoverybench/` | 239 real; 200 synthetic answer keys | Data-driven discovery evaluation |

Additional schema/count summary: `datasets/dataset_summary.json`.

## Dataset 1: RINoBench

- **Source**: Hugging Face `TimSchopf/RINoBench`
- **Format**: Parquet
- **Files**:
  - `datasets/rinobench/data/train-00000-of-00001.parquet`
  - `datasets/rinobench/data/test-00000-of-00001.parquet`
  - `datasets/rinobench/class_descriptions-00000-of-00001.parquet`
- **Columns**: `source`, `venueid`, `research_idea`, `novelty_score`, `novelty_reasoning`, `related_works`
- **Sample**: `datasets/rinobench/samples/sample.json`

Download:
```bash
mkdir -p datasets/rinobench/data
curl -L https://huggingface.co/datasets/TimSchopf/RINoBench/resolve/main/data/train-00000-of-00001.parquet -o datasets/rinobench/data/train-00000-of-00001.parquet
curl -L https://huggingface.co/datasets/TimSchopf/RINoBench/resolve/main/data/test-00000-of-00001.parquet -o datasets/rinobench/data/test-00000-of-00001.parquet
curl -L https://huggingface.co/datasets/TimSchopf/RINoBench/resolve/main/class_descriptions/class_descriptions-00000-of-00001.parquet -o datasets/rinobench/class_descriptions-00000-of-00001.parquet
```

Load:
```python
import pandas as pd
train = pd.read_parquet("datasets/rinobench/data/train-00000-of-00001.parquet")
test = pd.read_parquet("datasets/rinobench/data/test-00000-of-00001.parquet")
```

## Dataset 2: AI Idea Bench 2025

- **Source**: Hugging Face `yanshengqiu/AI_Idea_Bench_2025`
- **Format**: Parquet + JSON
- **Files**:
  - `datasets/ai_idea_bench_2025/test.parquet`
  - `datasets/ai_idea_bench_2025/target_paper_data.json`
- **Skipped**: `Idea_bench_data.zip` is about 30 GB; not downloaded.
- **Sample**: `datasets/ai_idea_bench_2025/samples/`

Download:
```bash
mkdir -p datasets/ai_idea_bench_2025
curl -L https://huggingface.co/datasets/yanshengqiu/AI_Idea_Bench_2025/resolve/main/test.parquet -o datasets/ai_idea_bench_2025/test.parquet
curl -L https://huggingface.co/datasets/yanshengqiu/AI_Idea_Bench_2025/resolve/main/target_paper_data.json -o datasets/ai_idea_bench_2025/target_paper_data.json
```

Load:
```python
import json
import pandas as pd
df = pd.read_parquet("datasets/ai_idea_bench_2025/test.parquet")
target = json.load(open("datasets/ai_idea_bench_2025/target_paper_data.json"))
```

## Dataset 3: ScienceAgentBench Annotations

- **Source**: Hugging Face `osunlp/ScienceAgentBench`
- **Format**: CSV + Parquet
- **Files**:
  - `datasets/scienceagentbench/ScienceAgentBench.csv`
  - `datasets/scienceagentbench/data/verified-00000-of-00001.parquet`
- **Note**: full benchmark data is hosted separately and password protected by the authors; README in `code/scienceagentbench/` documents access.

Download:
```bash
mkdir -p datasets/scienceagentbench/data
curl -L https://huggingface.co/datasets/osunlp/ScienceAgentBench/resolve/main/ScienceAgentBench.csv -o datasets/scienceagentbench/ScienceAgentBench.csv
curl -L https://huggingface.co/datasets/osunlp/ScienceAgentBench/resolve/main/data/verified-00000-of-00001.parquet -o datasets/scienceagentbench/data/verified-00000-of-00001.parquet
```

## Dataset 4: LiveIdeaBench v2 Sample

- **Source**: Hugging Face `6cf/liveideabench-v2`
- **Format**: CSV
- **Local file**: `datasets/liveideabench_sample/liveideabench_hf_head.csv`
- **Note**: full `liveideabench_hf.csv` is about 1.14 GB, so only the first 200 KB byte-range sample was downloaded.

Full download:
```bash
mkdir -p datasets/liveideabench_full
curl -L https://huggingface.co/datasets/6cf/liveideabench-v2/resolve/main/liveideabench_hf.csv -o datasets/liveideabench_full/liveideabench_hf.csv
```

## Dataset 5: IdeaBench

- **Source**: cloned from `code/ideabench/data/dataset/`
- **Files**:
  - `target_papers.csv`
  - `filtered_references.csv`
  - `raw_references.csv`
  - `ablation_target_papers.csv`
  - `ablation_filtered_references.csv`
  - `ideabench_clustering.json`
- **Sample**: `datasets/ideabench/samples/`

Load:
```python
import pandas as pd
targets = pd.read_csv("datasets/ideabench/target_papers.csv", encoding_errors="replace")
refs = pd.read_csv("datasets/ideabench/filtered_references.csv", encoding_errors="replace")
```

## Dataset 6: AI-Researcher Review Data

- **Source**: cloned from `code/ai_researcher_human_study/`
- **Files**:
  - `data_points_all_anonymized.json`
  - `id_title_mapping.csv`
  - `data_points_all_execution.json`
- **Use**: reviewer scores/rationales for ideation and execution-study records.

## Dataset 7: DiscoveryBench Answer Keys

- **Source**: cloned from `code/discoverybench/eval/`
- **Files**:
  - `answer_key_real.csv`
  - `answer_key_synth.csv`
- **Use**: target hypotheses for evaluating data-driven discovery outputs.
