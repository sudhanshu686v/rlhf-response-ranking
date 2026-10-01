import json
import requests
from pathlib import Path
import time

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5-coder:3b"

INPUT_FILE = Path("data/prompts.jsonl")
OUTPUT_FILE = Path("data/responses.jsonl")


def generate_response(prompt):
    data = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(
        OLLAMA_URL,
        json=data,
        timeout=180
    )

    response.raise_for_status()

    result = response.json()

    return result["response"]


# Load prompts
with open(INPUT_FILE, "r", encoding="utf-8") as file:
    prompts = [json.loads(line) for line in file]

print(f"Loaded {len(prompts)} prompts.")

# Generate 3 responses for every prompt
with open(OUTPUT_FILE, "w", encoding="utf-8") as output_file:

    for index, item in enumerate(prompts, start=1):

        prompt_id = item["id"]
        prompt = item["prompt"]

        print(f"\nProcessing {index}/{len(prompts)}: {prompt_id}")

        for response_number in range(1, 4):

            print(f"  Generating response {response_number}/3...")

            # Slightly different instruction for each candidate
            candidate_prompt = f"""
You are answering a coding-related question.

Give a correct, clear and useful answer.

Question:
{prompt}

This is candidate response {response_number}.
"""

            try:
                answer = generate_response(candidate_prompt)

                record = {
                    "prompt_id": prompt_id,
                    "category": item["category"],
                    "difficulty": item["difficulty"],
                    "prompt": prompt,
                    "response_id": f"{prompt_id}_response_{response_number}",
                    "response_number": response_number,
                    "response": answer
                }

                output_file.write(
                    json.dumps(record, ensure_ascii=False) + "\n"
                )

                output_file.flush()

            except Exception as error:
                print(f"  ERROR: {error}")

        # Small pause between prompts
        time.sleep(1)

print("\nFinished!")
print(f"Responses saved to: {OUTPUT_FILE}")
