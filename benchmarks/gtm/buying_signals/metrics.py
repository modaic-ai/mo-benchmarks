"""Binary probability metrics with signal-present as the positive class."""

from __future__ import annotations

import math


def percentile(values: list[float], fraction: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    position = (len(ordered) - 1) * fraction
    low = math.floor(position)
    high = math.ceil(position)
    return ordered[low] + (ordered[high] - ordered[low]) * (position - low)


def auroc(labels: list[int], scores: list[float]) -> float | None:
    positives = sum(labels)
    negatives = len(labels) - positives
    if positives == 0 or negatives == 0:
        return None
    ranked = sorted(zip(scores, labels, strict=True))
    positive_ranks = 0.0
    start = 0
    while start < len(ranked):
        end = start + 1
        while end < len(ranked) and ranked[end][0] == ranked[start][0]:
            end += 1
        positive_ranks += ((start + 1 + end) / 2) * sum(label for _, label in ranked[start:end])
        start = end
    return (positive_ranks - positives * (positives + 1) / 2) / (positives * negatives)


def summarize(labels: list[int], scores: list[float], threshold: float = 0.5) -> dict[str, float | int | None]:
    if not labels or len(labels) != len(scores) or any(label not in (0, 1) for label in labels):
        raise ValueError("Need nonempty equal-length binary labels and scores")
    if any(not math.isfinite(score) or not 0 <= score <= 1 for score in scores):
        raise ValueError("Probabilities must be finite and in [0, 1]")
    tp = sum(label == 1 and score >= threshold for label, score in zip(labels, scores, strict=True))
    fp = sum(label == 0 and score >= threshold for label, score in zip(labels, scores, strict=True))
    fn = sum(label == 1 and score < threshold for label, score in zip(labels, scores, strict=True))
    tn = len(labels) - tp - fp - fn
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    bins: list[list[tuple[int, float]]] = [[] for _ in range(10)]
    for label, score in zip(labels, scores, strict=True):
        bins[min(int(score * 10), 9)].append((label, score))
    ece = sum(
        len(items) / len(labels) * abs(
            sum(score for _, score in items) / len(items)
            - sum(label for label, _ in items) / len(items)
        )
        for items in bins if items
    )
    return {
        "n": len(labels), "positive": sum(labels), "negative": len(labels) - sum(labels),
        "tp": tp, "fp": fp, "tn": tn, "fn": fn,
        "f1": f1, "precision": precision, "recall": recall,
        "accuracy": (tp + tn) / len(labels), "auroc": auroc(labels, scores), "ece": ece,
    }
