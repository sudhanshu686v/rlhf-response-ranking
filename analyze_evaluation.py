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


print("=" * 50)
print("BASE MODEL vs SFT MODEL")
print("=" * 50)

print(f"\nTotal evaluations: {len(evaluations)}")


# -----------------------------
# Calculate average scores
# -----------------------------

print("\nAverage Scores")
print("-" * 50)

for model in ["base", "sft"]:

    print(f"\n{model.upper()} MODEL")

    total_score = 0

    for metric in metrics:

        average = sum(
            item[model][metric]
            for item in evaluations
        ) / len(evaluations)

        total_score += average

        print(
            f"{metric.replace('_', ' ').title():25}: "
            f"{average:.2f}"
        )

    overall = total_score / len(metrics)

    print(f"{'Overall Average':25}: {overall:.2f}")


# -----------------------------
# Winner distribution
# -----------------------------

print("\n\nWinner Distribution")
print("-" * 50)

winners = Counter(
    item["winner"]
    for item in evaluations
)

for winner, count in winners.items():

    percentage = (
        count / len(evaluations)
    ) * 100

    print(
        f"{winner:20}: "
        f"{count} ({percentage:.1f}%)"
    )


# -----------------------------
# Score differences
# -----------------------------

print("\n\nSFT - Base Score Difference")
print("-" * 50)

for metric in metrics:

    base_average = sum(
        item["base"][metric]
        for item in evaluations
    ) / len(evaluations)

    sft_average = sum(
        item["sft"][metric]
        for item in evaluations
    ) / len(evaluations)

    difference = sft_average - base_average

    print(
        f"{metric.replace('_', ' ').title():25}: "
        f"{difference:+.2f}"
    )


print("\nAnalysis complete!")