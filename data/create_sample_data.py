import json
import os

DATA_PATH = "data/sample_data.jsonl"

# Ensure the data directory exists
os.makedirs("data", exist_ok=True)

# Sample data
data = [
    {"id": 1, "text": "The stock market saw a significant rise today due to positive economic indicators."},
    {"id": 2, "text": "Apple Inc. announced a new line of MacBooks with M3 chips, boosting its stock price."},
    {"id": 3, "text": "Federal Reserve Chair hints at possible interest rate cuts in the next quarter."},
    {"id": 4, "text": "Tesla's new electric vehicle model outperforms previous versions in battery efficiency."},
    {"id": 5, "text": "Microsoft partners with OpenAI to integrate GPT-4 into its cloud services."},
    {"id": 6, "text": "Gold prices surge as investors seek safe-haven assets amid geopolitical tensions."}
]

# Write the sample data
with open(DATA_PATH, "w", encoding="utf-8") as f:
    for entry in data:
        f.write(json.dumps(entry) + "\n")

print("✅ `data/sample_data.jsonl` created successfully!")
