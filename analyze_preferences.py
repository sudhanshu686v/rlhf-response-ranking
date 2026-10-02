import json
from collections import Counter

FILE = "data/preference_dataset.jsonl"

pairs = []

with open(FILE, "r", encoding="utf-8") as file:
    for line in file:
        pairs.append(json.loads(line))


print("===== Preference Dataset Analysis =====")

print(f"Total preference pairs: {len(pairs)}")

# Categories
categories = Counter()

# Issue types
issues = Counter()

for item in pairs:
    prompt = item["prompt"].lower()

    if "python" in prompt:
        categories["Python"] += 1
    elif "c++" in prompt:
        categories["C++"] += 1
    elif "java" in prompt:
        categories["Java"] += 1
    elif "sql" in prompt or "database" in prompt:
        categories["SQL/DBMS"] += 1
    else:
        categories["DSA/Other"] += 1

    for issue in item.get("issues", []):
        issues[issue] += 1


print("\nCategory distribution:")

for category, count in categories.items():
    print(f"{category}: {count}")


print("\nIssue distribution:")

if issues:
    for issue, count in issues.most_common():
        print(f"{issue}: {count}")
else:
    print("No issues were tagged.")


# Check missing values

missing = 0

for item in pairs:

    if not item.get("prompt"):
        missing += 1

    if not item.get("chosen"):
        missing += 1

    if not item.get("rejected"):
        missing += 1


print(f"\nMissing required fields: {missing}")

print("\nAnalysis complete.")