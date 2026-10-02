import torch
from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
)
from peft import LoraConfig
from trl import SFTTrainer, SFTConfig


MODEL_NAME = "Qwen/Qwen2.5-Coder-1.5B-Instruct"
DATASET_PATH = "data/sft_dataset.jsonl"
OUTPUT_DIR = "models/qwen-coder-sft"


# -----------------------------
# Check GPU
# -----------------------------

if not torch.cuda.is_available():
    raise RuntimeError("CUDA GPU is not available.")

print("Using GPU:")
print(torch.cuda.get_device_name(0))


# -----------------------------
# Load dataset
# -----------------------------

dataset = load_dataset(
    "json",
    data_files=DATASET_PATH,
    split="train"
)

print(f"Training examples: {len(dataset)}")


# -----------------------------
# Convert dataset to text
# -----------------------------

def format_example(example):
    return {
        "text": (
            "### Instruction:\n"
            + example["instruction"]
            + "\n\n"
            "### Response:\n"
            + example["response"]
        )
    }


dataset = dataset.map(format_example)


# -----------------------------
# Tokenizer
# -----------------------------

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME
)

if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token


# -----------------------------
# Model
# -----------------------------

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float16,
)

model.config.use_cache = False


# -----------------------------
# LoRA
# -----------------------------

lora_config = LoraConfig(
    r=8,
    lora_alpha=16,
    lora_dropout=0.05,
    target_modules=[
        "q_proj",
        "k_proj",
        "v_proj",
        "o_proj",
    ],
    bias="none",
    task_type="CAUSAL_LM",
)


# -----------------------------
# Training configuration
# -----------------------------

training_args = SFTConfig(
    output_dir=OUTPUT_DIR,

    num_train_epochs=3,

    per_device_train_batch_size=1,

    gradient_accumulation_steps=4,

    learning_rate=2e-4,

    logging_steps=1,

    save_strategy="epoch",

    fp16=True,

    report_to="none",

    dataset_text_field="text",

    max_length=512,
)


# -----------------------------
# Trainer
# -----------------------------

trainer = SFTTrainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
    processing_class=tokenizer,
    peft_config=lora_config,
)


# -----------------------------
# Train
# -----------------------------

print("\nStarting LoRA SFT training...\n")

trainer.train()


# -----------------------------
# Save adapter
# -----------------------------

trainer.save_model(OUTPUT_DIR)

print("\nTraining complete!")
print(f"Model adapter saved to: {OUTPUT_DIR}")