import json
from pathlib import Path


PREFERENCES_FILE = Path("data/preferences.jsonl")
RESPONSES_FILE = Path("data/responses.jsonl")
OUTPUT_FILE = Path("data/preference_dataset.jsonl")


# --------------------------------
# Load all generated responses
# --------------------------------

responses = {}

with open(RESPONSES_FILE, "r", encoding="utf-8") as file:

    for line in file:
        item = json.loads(line)

        responses[item["response_id"]] = item["response"]


print(f"Loaded {len(responses)} generated responses.")


# --------------------------------
# Convert human preferences
# --------------------------------

preference_pairs = []

skipped = 0

with open(PREFERENCES_FILE, "r", encoding="utf-8") as file:

    for line in file:

        evaluation = json.loads(line)

        preferred = evaluation["preferred"]

        response_a_id = evaluation["response_a_id"]
        response_b_id = evaluation["response_b_id"]

        # Skip evaluations where there is no clear winner
        if preferred not in ["Response A", "Response B"]:
            skipped += 1
            continue

        if response_a_id not in responses:
            print(f"Missing response: {response_a_id}")
            continue

        if response_b_id not in responses:
            print(f"Missing response: {response_b_id}")
            continue

        # Determine chosen and rejected
        if preferred == "Response A":

            chosen = responses[response_a_id]
            rejected = responses[response_b_id]

        else:

            chosen = responses[response_b_id]
            rejected = responses[response_a_id]

        pair = {
            "prompt_id": evaluation["prompt_id"],
            "prompt": evaluation["prompt"],
            "chosen": chosen,
            "rejected": rejected,
            "issues": evaluation.get("issues", []),
            "reason": evaluation.get("reason", "")
        }

        preference_pairs.append(pair)


# --------------------------------
# Save preference dataset
# --------------------------------

with open(OUTPUT_FILE, "w", encoding="utf-8") as file:

    for pair in preference_pairs:

        file.write(
            json.dumps(pair, ensure_ascii=False) + "\n"
        )


# --------------------------------
# Summary
# --------------------------------

print("\nPreference dataset created!")
print(f"Clear preference pairs: {len(preference_pairs)}")
print(f"Skipped evaluations: {skipped}")
print(f"Saved to: {OUTPUT_FILE}")
