import json
import random
import streamlit as st
from pathlib import Path


# -----------------------------
# File locations
# -----------------------------

RESPONSES_FILE = Path("data/responses.jsonl")
PREFERENCES_FILE = Path("data/preferences.jsonl")


# -----------------------------
# Load responses
# -----------------------------

@st.cache_data
def load_responses():
    responses = []

    with open(RESPONSES_FILE, "r", encoding="utf-8") as file:
        for line in file:
            responses.append(json.loads(line))

    return responses


# -----------------------------
# Get data
# -----------------------------

responses = load_responses()

# Group responses by prompt
prompt_groups = {}

for response in responses:
    prompt_id = response["prompt_id"]

    if prompt_id not in prompt_groups:
        prompt_groups[prompt_id] = []

    prompt_groups[prompt_id].append(response)


# -----------------------------
# Page configuration
# -----------------------------

st.set_page_config(
    page_title="RLHF Response Ranking",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 RLHF Response Ranking Tool")

st.write(
    "Compare two AI-generated responses and choose the better one."
)


# -----------------------------
# Select prompt
# -----------------------------

prompt_ids = list(prompt_groups.keys())

if "current_prompt" not in st.session_state:
    st.session_state.current_prompt = random.choice(prompt_ids)

current_prompt_id = st.session_state.current_prompt

current_responses = prompt_groups[current_prompt_id]


# -----------------------------
# Display prompt
# -----------------------------

prompt_data = current_responses[0]

st.subheader("Question")

st.info(prompt_data["prompt"])

st.write(
    f"Category: **{prompt_data['category']}**  |  "
    f"Difficulty: **{prompt_data['difficulty']}**"
)


# -----------------------------
# Select two responses
# -----------------------------

if len(current_responses) >= 2:

    selected = random.sample(current_responses, 2)

    response_a = selected[0]
    response_b = selected[1]

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Response A")

        st.write(response_a["response"])

    with col2:
        st.subheader("Response B")

        st.write(response_b["response"])


    # -----------------------------
    # Ranking
    # -----------------------------

    st.subheader("Which response is better?")

    choice = st.radio(
        "Select one:",
        [
            "Response A",
            "Response B",
            "Both are similar",
            "Both are poor"
        ]
    )


    # -----------------------------
    # Issue tags
    # -----------------------------

    st.subheader("Issues")

    issues = st.multiselect(
        "Select any issues you notice:",
        [
            "Incorrect",
            "Hallucination",
            "Irrelevant",
            "Too verbose",
            "Too short",
            "Poor explanation",
            "Unsafe",
            "Biased",
            "Bad code",
            "Other"
        ]
    )

    reason = st.text_area(
        "Why did you prefer this response? (Optional)",
        placeholder="For example: Response A is more accurate and easier to understand."

    
    )



    # -----------------------------
    # Submit
    # -----------------------------

    if st.button("Submit Evaluation"):

        evaluation = {
            "prompt_id": current_prompt_id,
            "prompt": prompt_data["prompt"],
            "response_a_id": response_a["response_id"],
            "response_b_id": response_b["response_id"],
            "preferred": choice,
            "issues": issues,
            "reason": reason
        }

        with open(
            PREFERENCES_FILE,
            "a",
            encoding="utf-8"
        ) as file:

            file.write(
                json.dumps(evaluation) + "\n"
            )

        st.success("Evaluation saved!")

        st.session_state.current_prompt = random.choice(prompt_ids)

        st.rerun()