import json
from collections import Counter


FILE = "data/evaluation_results.jsonl"

with open(FILE, "r", encoding="utf-8") as file:
    evaluations = [
        json.loads(line)
        for line in file
    ]


metrics = [
    "correctness",
    "relevance",
    "clarity",
    "instruction_following"
]


# ==========================================
# Calculate model averages
# ==========================================

base_metric_averages = {}
sft_metric_averages = {}

for metric in metrics:

    base_average = sum(
        item["base"][metric]
        for item in evaluations
    ) / len(evaluations)

    sft_average = sum(
        item["sft"][metric]
        for item in evaluations
    ) / len(evaluations)

    base_metric_averages[metric] = base_average
    sft_metric_averages[metric] = sft_average


base_overall = sum(base_metric_averages.values()) / len(metrics)
sft_overall = sum(sft_metric_averages.values()) / len(metrics)

overall_difference = sft_overall - base_overall


# ==========================================
# Preference win rate
# ==========================================

winners = Counter(
    item["winner"]
    for item in evaluations
)

total = len(evaluations)

base_win_rate = (
    winners.get("Base Model", 0) / total
) * 100

sft_win_rate = (
    winners.get("SFT Model", 0) / total
) * 100


# ==========================================
# Print final report
# ==========================================

print("=" * 60)
print("FINAL RLHF EVALUATION REPORT")
print("=" * 60)

print(f"\nTotal Evaluations: {total}")


print("\nAverage Scores")
print("-" * 60)

print(
    f"{'Metric':25}"
    f"{'Base':>10}"
    f"{'SFT':>10}"
    f"{'Difference':>15}"
)

print("-" * 60)

for metric in metrics:

    difference = (
        sft_metric_averages[metric]
        - base_metric_averages[metric]
    )

    print(
        f"{metric.replace('_', ' ').title():25}"
        f"{base_metric_averages[metric]:>10.2f}"
        f"{sft_metric_averages[metric]:>10.2f}"
        f"{difference:>+15.2f}"
    )


print("-" * 60)

print(
    f"{'Overall Average':25}"
    f"{base_overall:>10.2f}"
    f"{sft_overall:>10.2f}"
    f"{overall_difference:>+15.2f}"
)


print("\nPreference Results")
print("-" * 60)

print(
    f"Base Model Wins : "
    f"{winners.get('Base Model', 0)} "
    f"({base_win_rate:.1f}%)"
)

print(
    f"SFT Model Wins  : "
    f"{winners.get('SFT Model', 0)} "
    f"({sft_win_rate:.1f}%)"
)

print(
    f"Similar          : "
    f"{winners.get('Both are similar', 0)} "
    f"({winners.get('Both are similar', 0) / total * 100:.1f}%)"
)


print("\nEvaluation complete!")
