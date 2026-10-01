import requests

url = "http://localhost:11434/api/generate"

data = {
    "model": "qwen2.5-coder:3b",
    "prompt": "Explain binary search in simple terms.",
    "stream": False
}

response = requests.post(url, json=data)

print("Status Code:", response.status_code)

result = response.json()

print("\nModel Response:")
print(result["response"])