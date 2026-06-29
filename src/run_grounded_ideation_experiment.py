"""Run grounded-novelty idea-generation experiments with real LLM API calls.

The script samples AI Idea Bench contexts, generates one idea per prompt
condition, evaluates each idea with an independent judge model, and caches all
raw responses so interrupted runs can resume safely.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import re
import subprocess
import sys
import time
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import requests
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "datasets" / "ai_idea_bench_2025" / "test.parquet"
RESULTS = ROOT / "results"
MODEL_OUTPUTS = RESULTS / "model_outputs"

SEED = 42
DEFAULT_GENERATION_MODEL = os.getenv("GENERATION_MODEL", "openai/gpt-4.1-mini")
DEFAULT_JUDGE_MODEL = os.getenv("JUDGE_MODEL", "google/gemini-2.5-flash")

CONDITIONS = [
    "ungrounded",
    "deduction",
    "induction",
    "proposal",
    "outcome_imagination",
    "small_experiment",
    "literature_comparison",
]

STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "in",
    "into",
    "is",
    "it",
    "of",
    "on",
    "or",
    "that",
    "the",
    "this",
    "to",
    "using",
    "with",
    "via",
    "towards",
    "toward",
    "large",
    "learning",
    "model",
    "models",
    "neural",
    "deep",
}


@dataclass(frozen=True)
class Context:
    context_id: str
    source_index: int
    topic: str
    keywords: list[str]
    prior_work_titles: list[str]
    audit: dict[str, Any]


class ApiError(RuntimeError):
    """Raised when the OpenRouter API returns an error."""


def set_seed(seed: int = SEED) -> None:
    random.seed(seed)
    np.random.seed(seed)


def normalize_text(value: Any) -> str:
    text = "" if value is None else str(value)
    return re.sub(r"\s+", " ", text).strip()


def to_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, tuple):
        return list(value)
    if hasattr(value, "tolist"):
        return value.tolist()
    return [value]


def tokenize(text: str) -> list[str]:
    return [
        token
        for token in re.findall(r"[A-Za-z][A-Za-z0-9\-]{2,}", text.lower())
        if token not in STOPWORDS
    ]


def topic_from_summary(summary: dict[str, Any]) -> str:
    topic = normalize_text(summary.get("revised_topic", ""))
    topic = re.sub(r"^The topic of this paper is\s+", "", topic, flags=re.I)
    topic = topic.rstrip(".")
    return topic


def build_audit(topic: str, keywords: list[str], prior_titles: list[str]) -> dict[str, Any]:
    title_tokens = tokenize(" ".join(prior_titles))
    topic_tokens = set(tokenize(topic + " " + " ".join(keywords)))
    counts = Counter(title_tokens)
    repeated_terms = [term for term, count in counts.most_common(8) if count >= 2]
    common_terms = [term for term, _ in counts.most_common(8)]
    evaluation_terms = {
        "benchmark",
        "dataset",
        "evaluation",
        "metric",
        "robustness",
        "ablation",
        "human",
        "simulation",
        "causal",
    }
    mechanism_terms = {
        "retrieval",
        "graph",
        "agent",
        "memory",
        "feedback",
        "uncertainty",
        "alignment",
        "reasoning",
        "planning",
        "calibration",
        "multimodal",
    }
    missing_eval_cues = sorted(evaluation_terms - set(title_tokens))[:8]
    topic_not_in_titles = sorted(topic_tokens - set(title_tokens))[:8]
    mechanism_hits = sorted(set(title_tokens) & mechanism_terms)
    return {
        "top_prior_work_terms": common_terms,
        "repeated_prior_work_terms": repeated_terms,
        "topic_terms_underrepresented_in_titles": topic_not_in_titles,
        "mechanism_terms_already_present": mechanism_hits,
        "missing_evaluation_cues": missing_eval_cues,
        "n_prior_titles": len(prior_titles),
        "n_unique_title_terms": len(set(title_tokens)),
    }


def load_contexts(limit: int, seed: int) -> list[Context]:
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Missing dataset: {DATA_PATH}")
    df = pd.read_parquet(DATA_PATH)
    records: list[Context] = []
    for _, row in df.iterrows():
        summary = row.get("summary")
        find_cite = row.get("find_cite")
        if not isinstance(summary, dict) or not isinstance(find_cite, dict):
            continue
        topic = topic_from_summary(summary)
        split_topic = summary.get("split_topic", {})
        keywords = []
        if isinstance(split_topic, dict):
            keywords = [normalize_text(k) for k in to_list(split_topic.get("keyword"))]
        top_refs = find_cite.get("top_references", {})
        prior_titles = []
        if isinstance(top_refs, dict):
            prior_titles = [normalize_text(t) for t in to_list(top_refs.get("title"))]
        prior_titles = [t for t in prior_titles if t]
        if not topic or len(prior_titles) < 4:
            continue
        source_index = int(row.get("index"))
        context_id = f"aiidea_{source_index}"
        audit = build_audit(topic, keywords, prior_titles)
        records.append(
            Context(
                context_id=context_id,
                source_index=source_index,
                topic=topic,
                keywords=keywords[:5],
                prior_work_titles=prior_titles[:5],
                audit=audit,
            )
        )
    rng = random.Random(seed)
    rng.shuffle(records)
    selected = records[:limit]
    return selected


def idea_output_schema() -> str:
    return json.dumps(
        {
            "title": "short title",
            "problem": "specific research problem",
            "proposed_method": "concrete method, model, or system",
            "grounding_used": "how the idea used the provided grounding",
            "experiment_plan": "datasets, baselines, metrics, and ablations",
            "expected_outcome": "what result would support the idea",
            "risk_and_mitigation": "main risk and practical mitigation",
            "why_novel": "why this differs from the listed prior work",
            "feasibility_notes": "resources needed and why feasible",
        },
        indent=2,
    )


def condition_instruction(condition: str, context: Context) -> str:
    prior_lines = "\n".join(f"- {title}" for title in context.prior_work_titles)
    audit_json = json.dumps(context.audit, indent=2)
    if condition == "ungrounded":
        return (
            "Generate a novel AI research idea from the topic and keywords only. "
            "Do not use any provided literature list. Focus on an idea that is not "
            "merely an incremental benchmark extension."
        )
    if condition == "deduction":
        return (
            "Ground novelty through deduction. Treat the topic, keywords, and prior-work "
            "titles as constraints. State the implicit gap that follows from those "
            "constraints, then propose an idea that logically addresses that gap.\n\n"
            f"Prior work titles:\n{prior_lines}"
        )
    if condition == "induction":
        return (
            "Ground novelty through induction. Infer a trend from the prior-work titles, "
            "then propose a next-step idea that extends the trend without copying one "
            "reference.\n\n"
            f"Prior work titles:\n{prior_lines}"
        )
    if condition == "proposal":
        return (
            "Ground novelty by writing the idea as a compact research proposal. The "
            "proposal must specify motivation, method, datasets, baselines, metrics, "
            "and ablations, and it must distinguish itself from prior work.\n\n"
            f"Prior work titles:\n{prior_lines}"
        )
    if condition == "outcome_imagination":
        return (
            "Ground novelty by imagining outcomes before finalizing the idea. Consider "
            "one positive and one negative plausible experimental outcome, then choose "
            "an idea that would teach something useful in both cases.\n\n"
            f"Prior work titles:\n{prior_lines}"
        )
    if condition == "small_experiment":
        return (
            "Ground novelty in a small empirical audit over the provided prior-work "
            "metadata. Use the audit findings as evidence for what is saturated and "
            "what is underexplored, then propose an idea.\n\n"
            f"Prior work titles:\n{prior_lines}\n\n"
            f"Small audit results:\n{audit_json}"
        )
    if condition == "literature_comparison":
        return (
            "Ground novelty through explicit literature comparison. Compare the idea "
            "against each prior-work title and revise it so the final idea has a clear "
            "mechanistic or evaluative difference from all listed work.\n\n"
            f"Prior work titles:\n{prior_lines}"
        )
    raise ValueError(f"Unknown condition: {condition}")


def generation_messages(context: Context, condition: str) -> list[dict[str, str]]:
    user = f"""Research topic: {context.topic}
Keywords: {", ".join(context.keywords)}

Grounding condition: {condition}
Instruction:
{condition_instruction(condition, context)}

Return exactly one JSON object matching this schema:
{idea_output_schema()}

Constraints:
- Do not mention that you are an AI language model.
- Do not name the hidden target paper or claim access to it.
- Be specific enough that a graduate student could implement a first experiment.
- Keep each field concise, but include concrete datasets, baselines, and metrics where possible.
- Return JSON only, with no markdown fences."""
    return [
        {
            "role": "system",
            "content": (
                "You are a careful AI research scientist generating plausible, original "
                "scientific ideas. Balance novelty with feasibility and avoid vague claims."
            ),
        },
        {"role": "user", "content": user},
    ]


def evaluation_messages(context: Context, idea: dict[str, Any]) -> list[dict[str, str]]:
    prior_lines = "\n".join(f"- {title}" for title in context.prior_work_titles)
    user = f"""Evaluate the following generated scientific idea.

Research topic: {context.topic}
Keywords: {", ".join(context.keywords)}
Prior-work titles available to the generator/judge:
{prior_lines}

Generated idea JSON:
{json.dumps(idea, indent=2)}

Use this rubric:
- novelty: 1 means direct recombination or obvious next step; 5 means a clear new mechanism, evaluation, or framing relative to the prior work.
- feasibility: 1 means unrealistic or underspecified; 5 means implementable with realistic datasets, baselines, metrics, and compute.
- specificity: 1 means generic; 5 means concrete technical plan.
- grounding: 1 means no visible use of evidence/constraints; 5 means grounded while not copying prior work.
- risk_awareness: 1 means no credible risks; 5 means clear failure mode and mitigation.
- overall: 1 means weak scientific idea; 5 means strong idea worth prototyping.

Return exactly one JSON object with keys:
{{
  "novelty": integer 1-5,
  "feasibility": integer 1-5,
  "specificity": integer 1-5,
  "grounding": integer 1-5,
  "risk_awareness": integer 1-5,
  "overall": integer 1-5,
  "duplicate_like_prior": boolean,
  "strongest_point": string,
  "weakest_point": string,
  "critique": string
}}

Keep `strongest_point`, `weakest_point`, and `critique` each under 25 words.
Return JSON only, with no markdown fences."""
    return [
        {
            "role": "system",
            "content": (
                "You are an independent scientific reviewer. Be strict, calibrated, "
                "and concise. Do not reward verbosity alone."
            ),
        },
        {"role": "user", "content": user},
    ]


def prompt_hash(messages: list[dict[str, str]]) -> str:
    payload = json.dumps(messages, sort_keys=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def extract_json_object(text: str) -> dict[str, Any]:
    cleaned = text.strip()
    cleaned = re.sub(r"^```(?:json)?", "", cleaned, flags=re.I).strip()
    cleaned = re.sub(r"```$", "", cleaned).strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        relaxed = re.sub(r",(\s*[}\]])", r"\1", cleaned)
        try:
            return json.loads(relaxed)
        except json.JSONDecodeError:
            match = re.search(r"\{.*\}", relaxed, flags=re.S)
            if not match:
                raise
            return json.loads(match.group(0))


def openrouter_key() -> str:
    key = os.getenv("OPENROUTER_KEY") or os.getenv("OPENROUTER_API_KEY")
    if not key:
        raise RuntimeError("OPENROUTER_KEY or OPENROUTER_API_KEY is required for real LLM calls")
    return key


@retry(
    retry=retry_if_exception_type((requests.RequestException, ApiError)),
    wait=wait_exponential(multiplier=1, min=2, max=30),
    stop=stop_after_attempt(5),
)
def call_openrouter(
    model: str,
    messages: list[dict[str, str]],
    temperature: float,
    max_tokens: int,
    seed: int | None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    if seed is not None:
        payload["seed"] = seed
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {openrouter_key()}",
            "Content-Type": "application/json",
            "X-Title": "Grounded Novelty Research Experiment",
        },
        json=payload,
        timeout=90,
    )
    if response.status_code >= 400:
        raise ApiError(f"OpenRouter {response.status_code}: {response.text[:500]}")
    return response.json()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    records = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def append_jsonl(path: Path, record: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=True) + "\n")


def save_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=True)


def collect_environment(args: argparse.Namespace) -> dict[str, Any]:
    def run(cmd: list[str]) -> str:
        try:
            return subprocess.check_output(cmd, text=True, stderr=subprocess.STDOUT, timeout=20).strip()
        except Exception as exc:  # pragma: no cover - environment best effort
            return f"ERROR: {type(exc).__name__}: {exc}"

    packages = {}
    for package in ["numpy", "pandas", "scipy", "matplotlib", "seaborn", "sklearn", "statsmodels", "requests"]:
        try:
            module = __import__(package)
            packages[package] = getattr(module, "__version__", "unknown")
        except Exception:
            packages[package] = "not_installed"

    gpu = run(["bash", "-lc", "nvidia-smi --query-gpu=name,memory.total,memory.free --format=csv 2>/dev/null || echo NO_GPU"])
    return {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version,
        "packages": packages,
        "gpu": gpu,
        "generation_model": args.generation_model,
        "judge_model": args.judge_model,
        "temperature_generation": args.generation_temperature,
        "temperature_judge": args.judge_temperature,
        "sample_size": args.limit,
        "seed": args.seed,
        "conditions": args.conditions,
        "data_path": str(DATA_PATH.relative_to(ROOT)),
    }


def run_generation(
    contexts: list[Context],
    conditions: list[str],
    args: argparse.Namespace,
) -> None:
    generation_path = MODEL_OUTPUTS / "generations.jsonl"
    done = {
        (record["context_id"], record["condition"])
        for record in read_jsonl(generation_path)
        if record.get("parsed_ok")
    }

    total = len(contexts) * len(conditions)
    completed = len(done)
    for context in contexts:
        for condition in conditions:
            key = (context.context_id, condition)
            if key in done:
                continue
            completed += 1
            messages = generation_messages(context, condition)
            print(f"[generation {completed}/{total}] {context.context_id} {condition}", flush=True)
            started = time.time()
            raw = call_openrouter(
                args.generation_model,
                messages,
                temperature=args.generation_temperature,
                max_tokens=args.generation_max_tokens,
                seed=args.seed,
            )
            content = raw["choices"][0]["message"]["content"]
            parsed_ok = True
            try:
                parsed = extract_json_object(content)
            except Exception as exc:
                parsed_ok = False
                parsed = {"parse_error": f"{type(exc).__name__}: {exc}", "raw_content": content}
            record = {
                "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                "context_id": context.context_id,
                "source_index": context.source_index,
                "condition": condition,
                "model": args.generation_model,
                "prompt_hash": prompt_hash(messages),
                "messages": messages,
                "raw_response": raw,
                "content": content,
                "idea": parsed,
                "parsed_ok": parsed_ok,
                "latency_seconds": round(time.time() - started, 3),
            }
            append_jsonl(generation_path, record)
            time.sleep(args.sleep)


def run_evaluation(contexts: list[Context], args: argparse.Namespace) -> None:
    context_by_id = {context.context_id: context for context in contexts}
    generation_records = [r for r in read_jsonl(MODEL_OUTPUTS / "generations.jsonl") if r.get("parsed_ok")]
    evaluation_path = MODEL_OUTPUTS / "evaluations.jsonl"
    done = {
        (record["context_id"], record["condition"])
        for record in read_jsonl(evaluation_path)
        if record.get("parsed_ok")
    }

    pending = [
        record
        for record in generation_records
        if record["context_id"] in context_by_id and (record["context_id"], record["condition"]) not in done
    ]
    total = len(done) + len(pending)
    completed = len(done)
    for record in pending:
        completed += 1
        context = context_by_id[record["context_id"]]
        condition = record["condition"]
        messages = evaluation_messages(context, record["idea"])
        print(f"[evaluation {completed}/{total}] {context.context_id} {condition}", flush=True)
        started = time.time()
        raw = call_openrouter(
            args.judge_model,
            messages,
            temperature=args.judge_temperature,
            max_tokens=args.judge_max_tokens,
            seed=args.seed,
        )
        content = raw["choices"][0]["message"]["content"]
        parsed_ok = True
        try:
            parsed = extract_json_object(content)
        except Exception as exc:
            parsed_ok = False
            parsed = {"parse_error": f"{type(exc).__name__}: {exc}", "raw_content": content}
        eval_record = {
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "context_id": context.context_id,
            "source_index": context.source_index,
            "condition": condition,
            "model": args.judge_model,
            "prompt_hash": prompt_hash(messages),
            "messages": messages,
            "raw_response": raw,
            "content": content,
            "scores": parsed,
            "parsed_ok": parsed_ok,
            "latency_seconds": round(time.time() - started, 3),
        }
        append_jsonl(evaluation_path, eval_record)
        time.sleep(args.sleep)


def parse_conditions(value: str) -> list[str]:
    conditions = [part.strip() for part in value.split(",") if part.strip()]
    unknown = sorted(set(conditions) - set(CONDITIONS))
    if unknown:
        raise argparse.ArgumentTypeError(f"Unknown conditions: {unknown}")
    return conditions


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=12, help="Number of contexts to sample.")
    parser.add_argument("--seed", type=int, default=SEED)
    parser.add_argument("--conditions", type=parse_conditions, default=CONDITIONS)
    parser.add_argument("--generation-model", default=DEFAULT_GENERATION_MODEL)
    parser.add_argument("--judge-model", default=DEFAULT_JUDGE_MODEL)
    parser.add_argument("--generation-temperature", type=float, default=0.7)
    parser.add_argument("--judge-temperature", type=float, default=0.0)
    parser.add_argument("--generation-max-tokens", type=int, default=900)
    parser.add_argument("--judge-max-tokens", type=int, default=750)
    parser.add_argument("--sleep", type=float, default=0.2, help="Delay between API calls.")
    parser.add_argument("--skip-generation", action="store_true")
    parser.add_argument("--skip-evaluation", action="store_true")
    return parser.parse_args()


def main() -> None:
    os.chdir(ROOT)
    set_seed(SEED)
    args = parse_args()
    if isinstance(args.conditions, str):
        args.conditions = parse_conditions(args.conditions)
    contexts = load_contexts(args.limit, args.seed)
    if len(contexts) < args.limit:
        raise RuntimeError(f"Only found {len(contexts)} usable contexts; requested {args.limit}")
    RESULTS.mkdir(exist_ok=True)
    MODEL_OUTPUTS.mkdir(parents=True, exist_ok=True)
    save_json(RESULTS / "contexts.json", [asdict(context) for context in contexts])
    save_json(RESULTS / "environment.json", collect_environment(args))
    save_json(
        RESULTS / "prompt_templates.json",
        {
            "conditions": args.conditions,
            "idea_schema": json.loads(idea_output_schema()),
            "generation_model": args.generation_model,
            "judge_model": args.judge_model,
        },
    )
    if not args.skip_generation:
        run_generation(contexts, args.conditions, args)
    if not args.skip_evaluation:
        run_evaluation(contexts, args)
    print("Experiment run complete.", flush=True)


if __name__ == "__main__":
    main()
