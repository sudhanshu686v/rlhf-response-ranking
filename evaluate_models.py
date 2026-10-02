import json
import torch

from pathlib import Path
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel


# ---------------------------------------
# Model paths
# ---------------------------------------

MODEL_NAME = "Qwen/Qwen2.5-Coder-1.5B-Instruct"

ADAPTER_PATH = "models/qwen-coder-sft"

TEST_FILE = "data/test_prompts.jsonl"

BASE_OUTPUT = "data/base_results.jsonl"
SFT_OUTPUT = "data/sft_results.jsonl"


# ---------------------------------------
# Check GPU
# ---------------------------------------

if not torch.cuda.is_available():
    raise RuntimeError("CUDA GPU is not available.")

print("GPU:")
print(torch.cuda.get_device_name(0))


# ---------------------------------------
# Load tokenizer
# ---------------------------------------

print("\nLoading tokenizer...")

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME
)

if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token


# ---------------------------------------
# Load base model
# ---------------------------------------

print("\nLoading base model...")

base_model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    dtype=torch.float16,
    device_map="auto"
)

base_model.eval()


# ---------------------------------------
# Load SFT model
# ---------------------------------------

print("\nLoading SFT adapter...")

sft_model = PeftModel.from_pretrained(
    base_model,
    ADAPTER_PATH
)

sft_model.eval()


# ---------------------------------------
# Load test prompts
# ---------------------------------------

with open(TEST_FILE, "r", encoding="utf-8") as file:
    test_prompts = [
        json.loads(line)
        for line in file
    ]

print(f"\nTest prompts: {len(test_prompts)}")


# ---------------------------------------
# Generate answer
# ---------------------------------------

def generate_answer(model, prompt):

    messages = [
        {
            "role": "user",
            "content": prompt
        }
    ]

    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    inputs = tokenizer(
        text,
        return_tensors="pt"
    ).to(model.device)

    with torch.no_grad():

        output = model.generate(
            **inputs,
            max_new_tokens=300,
            temperature=0.7,
            do_sample=True,
            top_p=0.9
        )

    generated_tokens = output[0][inputs["input_ids"].shape[1]:]

    answer = tokenizer.decode(
        generated_tokens,
        skip_special_tokens=True
    )

    return answer.strip()


# ---------------------------------------
# Generate base model results
# ---------------------------------------

print("\nGenerating BASE model responses...\n")

with open(BASE_OUTPUT, "w", encoding="utf-8") as file:

    for index, item in enumerate(test_prompts, start=1):

        print(
            f"Base: {index}/{len(test_prompts)} "
            f"{item['id']}"
        )

        answer = generate_answer(
            base_model,
            item["prompt"]
        )

        result = {
            "id": item["id"],
            "category": item["category"],
            "prompt": item["prompt"],
            "response": answer
        }

        file.write(
            json.dumps(
                result,
                ensure_ascii=False
            ) + "\n"
        )


# ---------------------------------------
# Generate SFT model results
# ---------------------------------------

print("\nGenerating SFT model responses...\n")

with open(SFT_OUTPUT, "w", encoding="utf-8") as file:

    for index, item in enumerate(test_prompts, start=1):

        print(
            f"SFT: {index}/{len(test_prompts)} "
            f"{item['id']}"
        )

        answer = generate_answer(
            sft_model,
            item["prompt"]
        )

        result = {
            "id": item["id"],
            "category": item["category"],
            "prompt": item["prompt"],
            "response": answer
        }

        file.write(
            json.dumps(
                result,
                ensure_ascii=False
            ) + "\n"
        )


print("\nEvaluation generation complete!")

print(f"Base results: {BASE_OUTPUT}")
print(f"SFT results: {SFT_OUTPUT}")