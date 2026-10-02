import streamlit as st
import json
import os


BASE_FILE = "data/base_results.jsonl"
SFT_FILE = "data/sft_results.jsonl"
OUTPUT_FILE = "data/evaluation_results.jsonl"


def load_jsonl(filename):
    data = []

    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            data.append(json.loads(line))

    return data


base_results = load_jsonl(BASE_FILE)
sft_results = load_jsonl(SFT_FILE)

st.title("Base Model vs SFT Model Evaluation")

st.write(
    "Compare both models and score each response independently."
)

total = min(len(base_results), len(sft_results))

st.write(f"Total questions: {total}")


if "current_index" not in st.session_state:
    st.session_state.current_index = 0


index = st.session_state.current_index

if index < total:

    base_item = base_results[index]
    sft_item = sft_results[index]

    prompt = base_item["prompt"]

    st.subheader(f"Question {index + 1} of {total}")

    st.write("### Prompt")
    st.write(prompt)

    st.divider()

    # -------------------------
    # BASE MODEL
    # -------------------------

    st.header("Base Model Response")

    st.write(base_item["response"])

    st.subheader("Score Base Model")

    base_correctness = st.slider(
        "Base - Correctness",
        1,
        5,
        3,
        key=f"base_correctness_{index}"
    )

    base_relevance = st.slider(
        "Base - Relevance",
        1,
        5,
        3,
        key=f"base_relevance_{index}"
    )

    base_clarity = st.slider(
        "Base - Clarity",
        1,
        5,
        3,
        key=f"base_clarity_{index}"
    )

    base_instruction = st.slider(
        "Base - Instruction Following",
        1,
        5,
        3,
        key=f"base_instruction_{index}"
    )

    st.divider()

    # -------------------------
    # SFT MODEL
    # -------------------------

    st.header("SFT Model Response")

    st.write(sft_item["response"])

    st.subheader("Score SFT Model")

    sft_correctness = st.slider(
        "SFT - Correctness",
        1,
        5,
        3,
        key=f"sft_correctness_{index}"
    )

    sft_relevance = st.slider(
        "SFT - Relevance",
        1,
        5,
        3,
        key=f"sft_relevance_{index}"
    )

    sft_clarity = st.slider(
        "SFT - Clarity",
        1,
        5,
        3,
        key=f"sft_clarity_{index}"
    )

    sft_instruction = st.slider(
        "SFT - Instruction Following",
        1,
        5,
        3,
        key=f"sft_instruction_{index}"
    )

    st.divider()

    # -------------------------
    # WINNER
    # -------------------------

    winner = st.radio(
        "Which response is better overall?",
        [
            "Base Model",
            "SFT Model",
            "Both are similar"
        ],
        key=f"winner_{index}"
    )

    reason = st.text_area(
        "Why?",
        key=f"reason_{index}",
        placeholder="Explain briefly why you selected this winner."
    )

    if st.button("Save Evaluation", type="primary"):

        evaluation = {
            "id": base_item["id"],
            "prompt": prompt,

            "base": {
                "correctness": base_correctness,
                "relevance": base_relevance,
                "clarity": base_clarity,
                "instruction_following": base_instruction
            },

            "sft": {
                "correctness": sft_correctness,
                "relevance": sft_relevance,
                "clarity": sft_clarity,
                "instruction_following": sft_instruction
            },

            "winner": winner,
            "reason": reason
        }

        with open(
            OUTPUT_FILE,
            "a",
            encoding="utf-8"
        ) as file:

            file.write(
                json.dumps(
                    evaluation,
                    ensure_ascii=False
                ) + "\n"
            )

        st.success("Evaluation saved!")

        st.session_state.current_index += 1

        st.rerun()

else:

    st.success("All evaluations completed!")

    st.write(
        f"Evaluation file: `{OUTPUT_FILE}`"
    )