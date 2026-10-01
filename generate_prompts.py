import json
from pathlib import Path

prompts = []

# -------------------------
# Python prompts
# -------------------------
python_prompts = [
    ("easy", "What is a variable in Python? Explain with a simple example."),
    ("easy", "What is the difference between a list and a tuple in Python?"),
    ("easy", "How do you define a function in Python? Give an example."),
    ("easy", "What is a dictionary in Python? Give a simple example."),
    ("medium", "Explain list comprehension in Python with two examples."),
    ("medium", "What is the difference between shallow copy and deep copy in Python?"),
    ("medium", "Explain exception handling in Python using try and except."),
    ("medium", "What are lambda functions in Python? Give an example."),
    ("hard", "Explain Python decorators with a practical example."),
    ("hard", "Explain generators in Python and compare them with normal functions."),
]

# -------------------------
# C++ prompts
# -------------------------
cpp_prompts = [
    ("easy", "What is a pointer in C++? Explain with an example."),
    ("easy", "What is the difference between an array and a vector in C++?"),
    ("easy", "Explain classes and objects in C++ with an example."),
    ("easy", "What is a constructor in C++?"),
    ("medium", "Explain inheritance in C++ with an example."),
    ("medium", "What is function overloading in C++?"),
    ("medium", "Explain the difference between stack and heap memory in C++."),
    ("medium", "Explain STL vectors in C++ with common operations."),
    ("hard", "Explain virtual functions and runtime polymorphism in C++."),
    ("hard", "Explain smart pointers in C++ and why they are useful."),
]

# -------------------------
# Java prompts
# -------------------------
java_prompts = [
    ("easy", "What is a class in Java? Give an example."),
    ("easy", "What is the difference between == and equals() in Java?"),
    ("easy", "What is a constructor in Java?"),
    ("easy", "Explain the main method in Java."),
    ("medium", "Explain inheritance in Java with an example."),
    ("medium", "What is method overloading in Java?"),
    ("medium", "Explain the difference between ArrayList and LinkedList in Java."),
    ("medium", "What is exception handling in Java?"),
    ("hard", "Explain interfaces and abstract classes in Java."),
    ("hard", "Explain Java multithreading and thread synchronization."),
]

# -------------------------
# SQL / DBMS prompts
# -------------------------
sql_prompts = [
    ("easy", "What is a primary key in a database?"),
    ("easy", "What is a foreign key? Give an example."),
    ("easy", "What is the difference between DELETE and DROP in SQL?"),
    ("easy", "What is a relational database?"),
    ("medium", "Explain INNER JOIN with an SQL example."),
    ("medium", "What is database normalization? Explain 1NF and 2NF."),
    ("medium", "Explain GROUP BY and HAVING in SQL."),
    ("medium", "What is the difference between WHERE and HAVING?"),
    ("hard", "Explain BCNF with an example."),
    ("hard", "Explain database indexing and its advantages and disadvantages."),
]

# -------------------------
# DSA prompts
# -------------------------
dsa_prompts = [
    ("easy", "What is a stack? Explain its basic operations."),
    ("easy", "What is a queue? Explain its basic operations."),
    ("easy", "What is the difference between BFS and DFS?"),
    ("easy", "What is binary search?"),
    ("medium", "Explain binary search with C++ code."),
    ("medium", "Explain merge sort and its time complexity."),
    ("medium", "Explain quicksort and its average time complexity."),
    ("medium", "What is a binary search tree?"),
    ("hard", "Explain Dijkstra's shortest path algorithm."),
    ("hard", "Explain dynamic programming with a suitable example."),
]

# Combine all categories
categories = {
    "python": python_prompts,
    "cpp": cpp_prompts,
    "java": java_prompts,
    "sql_dbms": sql_prompts,
    "dsa": dsa_prompts,
}

prompt_id = 1

for category, questions in categories.items():
    for difficulty, question in questions:
        prompts.append({
            "id": f"prompt_{prompt_id:03d}",
            "category": category,
            "difficulty": difficulty,
            "prompt": question
        })
        prompt_id += 1

# Repeat the base questions with variations
base_prompts = prompts.copy()

while len(prompts) < 150:
    for item in base_prompts:
        if len(prompts) >= 150:
            break

        prompts.append({
            "id": f"prompt_{len(prompts) + 1:03d}",
            "category": item["category"],
            "difficulty": item["difficulty"],
            "prompt": item["prompt"] +
                      " Provide a clear explanation suitable for a beginner."
        })

# Save JSONL
output_file = Path("data/prompts.jsonl")

with open(output_file, "w", encoding="utf-8") as file:
    for prompt in prompts:
        file.write(json.dumps(prompt) + "\n")

print(f"Created {len(prompts)} prompts.")
print(f"Saved to: {output_file}")