import json
import matplotlib.pyplot as plt
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


# --------------------------------
# Calculate averages
# --------------------------------

base_scores = []
sft_scores = []

for metric in metrics:

    base_average = sum(
        item["base"][metric]
        for item in evaluations
    ) / len(evaluations)

    sft_average = sum(
        item["sft"][metric]
        for item in evaluations
    ) / len(evaluations)

    base_scores.append(base_average)
    sft_scores.append(sft_average)


# --------------------------------
# Chart 1: Metric comparison
# --------------------------------

x = range(len(metrics))

plt.figure(figsize=(10, 6))

plt.bar(
    [i - 0.2 for i in x],
    base_scores,
    width=0.4,
    label="Base Model"
)

plt.bar(
    [i + 0.2 for i in x],
    sft_scores,
    width=0.4,
    label="SFT Model"
)

plt.xticks(
    list(x),
    [
        "Correctness",
        "Relevance",
        "Clarity",
        "Instruction Following"
    ]
)

plt.ylabel("Average Score (1–5)")
plt.title("Base Model vs SFT Model")

plt.ylim(0, 5)
plt.legend()
plt.tight_layout()

plt.savefig(
    "data/metric_comparison.png",
    dpi=150
)

plt.show()


# --------------------------------
# Chart 2: Winner distribution
# --------------------------------

winners = Counter(
    item["winner"]
    for item in evaluations
)

labels = [
    "Base Model",
    "SFT Model",
    "Both Similar"
]

values = [
    winners.get("Base Model", 0),
    winners.get("SFT Model", 0),
    winners.get("Both are similar", 0)
]

plt.figure(figsize=(8, 5))

plt.bar(
    labels,
    values
)

plt.ylabel("Number of Evaluations")
plt.title("Model Preference Distribution")

plt.tight_layout()

plt.savefig(
    "data/winner_distribution.png",
    dpi=150
)

plt.show()


print("Charts created successfully!")

print("\nFiles:")
print("data/metric_comparison.png")
print("data/winner_distribution.png")