# RLHF Response Ranking & SFT Dataset Builder

A complete beginner-friendly pipeline for collecting human preferences between LLM responses, building preference and supervised fine-tuning datasets, and fine-tuning a coding LLM using LoRA.

## Project Overview

This project demonstrates a simplified RLHF-style workflow for improving LLM responses through human feedback.

The pipeline:

1. Create coding prompts
2. Generate multiple candidate responses using a local LLM
3. Compare responses using a Streamlit human evaluation interface
4. Build a preference dataset
5. Create an SFT dataset from preferred responses
6. Fine-tune a coding model using LoRA
7. Compare the base model against the SFT model
8. Analyze model performance

## Architecture

```text
                Coding Prompts
                     |
                     v
             +----------------+
             |  Ollama LLM    |
             | Qwen Coder 3B  |
             +----------------+
                     |
                     v
            Candidate Responses
                     |
                     v
          +-----------------------+
          | Streamlit Annotation  |
          | Human Preference UI   |
          +-----------------------+
                     |
                     v
            Preference Dataset
             chosen / rejected
                     |
                     v
              SFT Dataset
                     |
                     v
          +----------------------+
          | LoRA Fine-Tuning     |
          | Qwen Coder 1.5B      |
          +----------------------+
                     |
                     v
              SFT Adapter
                     |
                     v
          +----------------------+
          | Base vs SFT Testing  |
          +----------------------+
                     |
                     v
              Evaluation