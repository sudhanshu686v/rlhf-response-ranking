import json
from collections import Counter
from statistics import mean

FILE = "data/evaluation_results.jsonl"


# -----------------------------
# Load evaluations
# -----------------------------

evaluations = []

with open(FILE, "r", encoding="utf-8") as file:
    for line in file:
        evaluations.append(json.loads(line))


print("=" * 45)
print("BASE vs SFT EVALUATION")
print("=" * 45)

print(f"\nTotal evaluations: {len(evaluations)}")


# -----------------------------
# Winner distribution
# -----------------------------

winners = Counter(
    item["winner"]
    for item in evaluations
)

print("\nWinner distribution:")

for winner, count in winners.items():
    percentage = (count / len(evaluations)) * 100

    print(
        f"{winner}: {count} "
        f"({percentage:.1f}%)"
    )


# -----------------------------
# Average scores
# -----------------------------

metrics = [
    "correctness",
    "relevance",
    "clarity",
    "instruction_following"
]

print("\nAverage scores:")

for metric in metrics:

    scores = [
        item[metric]
        for item in evaluations
    ]

    print(
        f"{metric.replace('_', ' ').title()}: "
        f"{mean(scores):.2f}/5"
    )


# -----------------------------
# Individual model scores
# -----------------------------

# Calculate scores for questions
# where each model was selected
# as the winner.

print("\nWinner percentage:")

total = len(evaluations)

base_wins = winners.get("Base Model", 0)
sft_wins = winners.get("SFT Model", 0)
similar = winners.get("Both are similar", 0)

print(f"Base Model: {base_wins / total * 100:.1f}%")
print(f"SFT Model: {sft_wins / total * 100:.1f}%")
print(f"Similar: {similar / total * 100:.1f}%")


print("\nAnalysis complete.")