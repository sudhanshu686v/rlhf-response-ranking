import json
from pathlib import Path


INPUT_FILE = Path("data/preference_dataset.jsonl")
OUTPUT_FILE = Path("data/sft_dataset.jsonl")

TARGET_EXAMPLES = 40


# --------------------------------
# Load preference dataset
# --------------------------------

with open(INPUT_FILE, "r", encoding="utf-8") as file:
    pairs = [
        json.loads(line)
        for line in file
    ]


print(f"Loaded {len(pairs)} preference pairs.")


# --------------------------------
# Create SFT examples
# --------------------------------

sft_examples = []

seen_prompts = set()

for item in pairs:

    prompt = item["prompt"]
    chosen = item["chosen"]

    # Avoid duplicate prompts
    if prompt in seen_prompts:
        continue

    # Skip empty examples
    if not prompt.strip() or not chosen.strip():
        continue

    example = {
        "instruction": prompt,
        "response": chosen
    }

    sft_examples.append(example)

    seen_prompts.add(prompt)

    if len(sft_examples) >= TARGET_EXAMPLES:
        break


# --------------------------------
# Save SFT dataset
# --------------------------------

with open(OUTPUT_FILE, "w", encoding="utf-8") as file:

    for example in sft_examples:

        file.write(
            json.dumps(
                example,
                ensure_ascii=False
            ) + "\n"
        )


print("\nSFT dataset created!")
print(f"Examples: {len(sft_examples)}")
print(f"Saved to: {OUTPUT_FILE}")