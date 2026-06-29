"""Analyze grounded-novelty experiment outputs."""

from __future__ import annotations

import json
import math
import re
from itertools import combinations
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_distances


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
MODEL_OUTPUTS = RESULTS / "model_outputs"
TABLES = RESULTS / "tables"
EVALUATIONS = RESULTS / "evaluations"
FIGURES = ROOT / "figures"

CONDITION_ORDER = [
    "ungrounded",
    "deduction",
    "induction",
    "proposal",
    "outcome_imagination",
    "small_experiment",
    "literature_comparison",
]

SCORE_COLUMNS = ["novelty", "feasibility", "specificity", "grounding", "risk_awareness", "overall"]

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


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    records = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def flatten_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        return " ".join(flatten_text(v) for v in value.values())
    if isinstance(value, list):
        return " ".join(flatten_text(v) for v in value)
    return str(value)


def tokenize(text: str) -> list[str]:
    return [
        token
        for token in re.findall(r"[A-Za-z][A-Za-z0-9\-]{2,}", text.lower())
        if token not in STOPWORDS
    ]


def jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def bootstrap_ci(values: np.ndarray, seed: int = 42, n_boot: int = 5000) -> tuple[float, float]:
    values = values[~np.isnan(values)]
    if len(values) == 0:
        return math.nan, math.nan
    rng = np.random.default_rng(seed)
    means = []
    for _ in range(n_boot):
        sample = rng.choice(values, size=len(values), replace=True)
        means.append(float(np.mean(sample)))
    return float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))


def holm_adjust(p_values: list[float]) -> list[float]:
    """Holm-Bonferroni adjusted p-values preserving input order."""
    n = len(p_values)
    indexed = sorted(enumerate(p_values), key=lambda item: item[1])
    adjusted = [math.nan] * n
    running_max = 0.0
    for rank, (idx, p_value) in enumerate(indexed):
        adjusted_p = min(1.0, (n - rank) * p_value)
        running_max = max(running_max, adjusted_p)
        adjusted[idx] = running_max
    return adjusted


def paired_cohens_d(diff: np.ndarray) -> float:
    diff = diff[~np.isnan(diff)]
    if len(diff) < 2:
        return math.nan
    sd = np.std(diff, ddof=1)
    if sd == 0:
        return math.nan
    return float(np.mean(diff) / sd)


def load_contexts() -> dict[str, dict[str, Any]]:
    with (RESULTS / "contexts.json").open("r", encoding="utf-8") as handle:
        contexts = json.load(handle)
    return {context["context_id"]: context for context in contexts}


def build_dataframe() -> pd.DataFrame:
    contexts = load_contexts()
    generations = {
        (record["context_id"], record["condition"]): record
        for record in read_jsonl(MODEL_OUTPUTS / "generations.jsonl")
        if record.get("parsed_ok")
    }
    evaluations = {
        (record["context_id"], record["condition"]): record
        for record in read_jsonl(MODEL_OUTPUTS / "evaluations.jsonl")
        if record.get("parsed_ok")
    }
    rows = []
    for key, gen in generations.items():
        if key not in evaluations or gen["context_id"] not in contexts:
            continue
        context = contexts[gen["context_id"]]
        eval_record = evaluations[key]
        scores = eval_record.get("scores", {})
        idea = gen.get("idea", {})
        idea_text = flatten_text(idea)
        idea_tokens = set(tokenize(idea_text))
        prior_titles = context.get("prior_work_titles", [])
        prior_text = " ".join(prior_titles)
        prior_tokens = set(tokenize(prior_text))
        title_tokens = set(tokenize(str(idea.get("title", ""))))
        prior_title_jaccards = [jaccard(title_tokens, set(tokenize(title))) for title in prior_titles]
        unique_tokens = max(1, len(idea_tokens))
        row = {
            "context_id": gen["context_id"],
            "source_index": gen.get("source_index"),
            "condition": gen["condition"],
            "topic": context.get("topic"),
            "keywords": ", ".join(context.get("keywords", [])),
            "idea_title": idea.get("title", ""),
            "idea_text": idea_text,
            "word_count": len(idea_text.split()),
            "prior_overlap_fraction": len(idea_tokens & prior_tokens) / unique_tokens,
            "prior_title_max_jaccard": max(prior_title_jaccards) if prior_title_jaccards else 0.0,
            "duplicate_like_prior": bool(scores.get("duplicate_like_prior", False)),
            "strongest_point": scores.get("strongest_point", ""),
            "weakest_point": scores.get("weakest_point", ""),
            "critique": scores.get("critique", ""),
            "generation_latency_seconds": gen.get("latency_seconds"),
            "evaluation_latency_seconds": eval_record.get("latency_seconds"),
        }
        for col in SCORE_COLUMNS:
            row[col] = pd.to_numeric(scores.get(col), errors="coerce")
        rows.append(row)
    df = pd.DataFrame(rows)
    if df.empty:
        raise RuntimeError("No complete generation/evaluation pairs found.")
    df["condition"] = pd.Categorical(df["condition"], categories=CONDITION_ORDER, ordered=True)
    df["composite_mean"] = df[SCORE_COLUMNS].mean(axis=1)
    df["quality_mean"] = df[["novelty", "feasibility", "specificity", "grounding", "overall"]].mean(axis=1)
    df["novelty_feasibility_product"] = df["novelty"] * df["feasibility"]
    df["automatic_novelty_proxy"] = 1.0 - df["prior_overlap_fraction"]
    return df.sort_values(["context_id", "condition"]).reset_index(drop=True)


def add_diversity(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["condition_diversity"] = np.nan
    for condition, group in df.groupby("condition", observed=True):
        if len(group) < 2:
            continue
        vectorizer = TfidfVectorizer(stop_words="english", min_df=1)
        matrix = vectorizer.fit_transform(group["idea_text"].fillna(""))
        distances = cosine_distances(matrix)
        upper = distances[np.triu_indices_from(distances, k=1)]
        diversity = float(np.mean(upper)) if len(upper) else math.nan
        df.loc[group.index, "condition_diversity"] = diversity
    return df


def summarize_conditions(df: pd.DataFrame) -> pd.DataFrame:
    metrics = SCORE_COLUMNS + [
        "composite_mean",
        "quality_mean",
        "novelty_feasibility_product",
        "prior_overlap_fraction",
        "prior_title_max_jaccard",
        "automatic_novelty_proxy",
        "word_count",
        "condition_diversity",
    ]
    rows = []
    for condition, group in df.groupby("condition", observed=True):
        row: dict[str, Any] = {"condition": condition, "n": len(group)}
        for metric in metrics:
            values = group[metric].astype(float).to_numpy()
            ci_low, ci_high = bootstrap_ci(values)
            row[f"{metric}_mean"] = float(np.nanmean(values))
            row[f"{metric}_std"] = float(np.nanstd(values, ddof=1)) if len(values) > 1 else math.nan
            row[f"{metric}_median"] = float(np.nanmedian(values))
            row[f"{metric}_ci_low"] = ci_low
            row[f"{metric}_ci_high"] = ci_high
        rows.append(row)
    return pd.DataFrame(rows)


def run_stat_tests(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    test_metrics = [
        "novelty",
        "feasibility",
        "specificity",
        "grounding",
        "overall",
        "quality_mean",
        "novelty_feasibility_product",
        "prior_overlap_fraction",
    ]
    omnibus_rows = []
    pairwise_rows = []
    for metric in test_metrics:
        pivot = df.pivot_table(index="context_id", columns="condition", values=metric, observed=True)
        pivot = pivot.dropna(axis=0)
        available_conditions = [c for c in CONDITION_ORDER if c in pivot.columns]
        if len(available_conditions) >= 3 and len(pivot) >= 2:
            arrays = [pivot[c].to_numpy() for c in available_conditions]
            stat, p_value = stats.friedmanchisquare(*arrays)
            omnibus_rows.append(
                {
                    "metric": metric,
                    "test": "Friedman",
                    "n_contexts": len(pivot),
                    "conditions": ",".join(available_conditions),
                    "statistic": float(stat),
                    "p_value": float(p_value),
                }
            )
        if "ungrounded" not in pivot.columns:
            continue
        raw_rows = []
        for condition in available_conditions:
            if condition == "ungrounded":
                continue
            diff = (pivot[condition] - pivot["ungrounded"]).astype(float).to_numpy()
            if len(diff) < 2 or np.allclose(diff, 0):
                stat = 0.0
                p_value = 1.0
            else:
                stat, p_value = stats.wilcoxon(
                    pivot[condition],
                    pivot["ungrounded"],
                    zero_method="zsplit",
                    alternative="two-sided",
                )
            raw_rows.append(
                {
                    "metric": metric,
                    "condition": condition,
                    "baseline": "ungrounded",
                    "n_contexts": len(pivot),
                    "mean_diff": float(np.nanmean(diff)),
                    "median_diff": float(np.nanmedian(diff)),
                    "paired_cohens_d": paired_cohens_d(diff),
                    "wilcoxon_statistic": float(stat),
                    "p_value": float(p_value),
                }
            )
        adjusted = holm_adjust([row["p_value"] for row in raw_rows])
        for row, p_adj in zip(raw_rows, adjusted):
            row["holm_p_value"] = p_adj
            pairwise_rows.append(row)
    return pd.DataFrame(omnibus_rows), pd.DataFrame(pairwise_rows)


def make_figures(df: pd.DataFrame, summary: pd.DataFrame) -> None:
    sns.set_theme(style="whitegrid", context="notebook")
    FIGURES.mkdir(parents=True, exist_ok=True)

    plot_df = df.melt(
        id_vars=["context_id", "condition"],
        value_vars=["novelty", "feasibility", "specificity", "grounding", "overall"],
        var_name="metric",
        value_name="score",
    )
    plt.figure(figsize=(12, 6))
    sns.barplot(data=plot_df, x="condition", y="score", hue="metric", errorbar=("ci", 95))
    plt.xticks(rotation=25, ha="right")
    plt.ylim(1, 5)
    plt.xlabel("Prompt condition")
    plt.ylabel("Judge score (1-5)")
    plt.title("Judged Idea Quality by Grounding Condition")
    plt.tight_layout()
    plt.savefig(FIGURES / "condition_scores.png", dpi=200)
    plt.close()

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    sns.barplot(data=df, x="condition", y="prior_overlap_fraction", errorbar=("ci", 95), ax=axes[0])
    axes[0].tick_params(axis="x", rotation=25)
    axes[0].set_title("Prior-Work Title Token Overlap")
    axes[0].set_xlabel("Prompt condition")
    axes[0].set_ylabel("Overlap fraction")
    sns.barplot(data=df, x="condition", y="condition_diversity", errorbar=None, ax=axes[1])
    axes[1].tick_params(axis="x", rotation=25)
    axes[1].set_title("Within-Condition TF-IDF Diversity")
    axes[1].set_xlabel("Prompt condition")
    axes[1].set_ylabel("Mean pairwise cosine distance")
    plt.tight_layout()
    plt.savefig(FIGURES / "overlap_diversity.png", dpi=200)
    plt.close()

    plt.figure(figsize=(10, 5))
    sns.barplot(
        data=df,
        x="condition",
        y="novelty_feasibility_product",
        errorbar=("ci", 95),
    )
    plt.xticks(rotation=25, ha="right")
    plt.xlabel("Prompt condition")
    plt.ylabel("Novelty x feasibility (1-25)")
    plt.title("Novelty-Feasibility Tradeoff")
    plt.tight_layout()
    plt.savefig(FIGURES / "novelty_feasibility_product.png", dpi=200)
    plt.close()


def write_error_analysis(df: pd.DataFrame) -> None:
    lines = ["# Error Analysis\n"]
    for condition, group in df.groupby("condition", observed=True):
        sorted_group = group.sort_values(["overall", "novelty_feasibility_product"], ascending=[True, True])
        worst = sorted_group.iloc[0]
        best = sorted_group.iloc[-1]
        lines.append(f"## {condition}\n")
        lines.append(
            f"- Best example: `{best['context_id']}` / {best['idea_title']} "
            f"(overall={best['overall']}, novelty={best['novelty']}, feasibility={best['feasibility']}). "
            f"Strongest point: {best['strongest_point']}\n"
        )
        lines.append(
            f"- Weakest example: `{worst['context_id']}` / {worst['idea_title']} "
            f"(overall={worst['overall']}, novelty={worst['novelty']}, feasibility={worst['feasibility']}). "
            f"Weakest point: {worst['weakest_point']}\n"
        )
    EVALUATIONS.mkdir(parents=True, exist_ok=True)
    (EVALUATIONS / "error_analysis.md").write_text("\n".join(lines), encoding="utf-8")


def write_analysis_summary(
    df: pd.DataFrame,
    summary: pd.DataFrame,
    omnibus: pd.DataFrame,
    pairwise: pd.DataFrame,
) -> None:
    best_overall = summary.sort_values("overall_mean", ascending=False).iloc[0]
    best_product = summary.sort_values("novelty_feasibility_product_mean", ascending=False).iloc[0]
    baseline = summary[summary["condition"] == "ungrounded"].iloc[0]
    lines = [
        "# Analysis Summary",
        "",
        f"Complete idea/evaluation pairs: {len(df)} across {df['context_id'].nunique()} contexts.",
        f"Best mean overall score: {best_overall['condition']} ({best_overall['overall_mean']:.2f}).",
        (
            "Best mean novelty-feasibility product: "
            f"{best_product['condition']} ({best_product['novelty_feasibility_product_mean']:.2f})."
        ),
        f"Ungrounded baseline mean overall: {baseline['overall_mean']:.2f}.",
        "",
        "## Omnibus Tests",
        "",
        omnibus.to_markdown(index=False) if not omnibus.empty else "No omnibus tests available.",
        "",
        "## Pairwise Tests vs Ungrounded",
        "",
        pairwise.to_markdown(index=False) if not pairwise.empty else "No pairwise tests available.",
    ]
    (RESULTS / "analysis_summary.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    TABLES.mkdir(parents=True, exist_ok=True)
    EVALUATIONS.mkdir(parents=True, exist_ok=True)
    df = build_dataframe()
    df = add_diversity(df)
    summary = summarize_conditions(df)
    omnibus, pairwise = run_stat_tests(df)
    df.to_csv(TABLES / "idea_level_scores.csv", index=False)
    summary.to_csv(TABLES / "condition_summary.csv", index=False)
    omnibus.to_csv(TABLES / "omnibus_tests.csv", index=False)
    pairwise.to_csv(TABLES / "pairwise_tests_vs_ungrounded.csv", index=False)
    make_figures(df, summary)
    write_error_analysis(df)
    write_analysis_summary(df, summary, omnibus, pairwise)
    print(f"Analyzed {len(df)} complete records across {df['context_id'].nunique()} contexts.")
    print(f"Wrote tables to {TABLES.relative_to(ROOT)} and figures to {FIGURES.relative_to(ROOT)}.")


if __name__ == "__main__":
    main()
