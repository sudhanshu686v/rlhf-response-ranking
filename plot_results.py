import json
import matplotlib.pyplot as plt
from collections import Counter


FILE = "data/evaluation_results.jsonl"


with open(FILE, "r", encoding="utf-8") as file:
    evaluations = [
        json.loads(line)
        for line in file
    ]


# -----------------------------
# Winner chart
# -----------------------------

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

plt.bar(labels, values)

plt.title("Base Model vs SFT Model")
plt.xlabel("Model")
plt.ylabel("Number of Wins")

plt.tight_layout()

plt.savefig(
    "data/model_comparison.png",
    dpi=150
)

plt.show()


print("Chart saved to data/model_comparison.png")