import pandas as pd
import subprocess
import json

MODEL = "llama3.2:1b"

def query_ollama(prompt, model=MODEL):
    """Send a prompt to Ollama and return its raw output."""
    result = subprocess.run(
        ["ollama", "run", model],
        input=prompt.encode("utf-8"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout.decode("utf-8").strip()

def parse_row_with_llm(row: pd.Series):
    """Use Ollama to extract name and quantity from a DataFrame row."""
    # Convert row (Series) to dict for clarity
    row_dict = row.to_dict()

    prompt = f"""
You are a data extraction model. Interpret the following dictionary representing one row of a CSV file:

{json.dumps(row_dict)}

Your task:
- Identify which field in this row refers to the hardware part or item name.
- Identify which field refers to the numeric quantity.

Return a **single JSON object only**, with exactly these two keys:
  {{
    "name": "<part or item name, string>",
    "quantity": <integer or float quantity, set as integer in output>
  }}

Rules:
- Output only valid JSON (no markdown, no explanations, no code).
- If a field is missing, output `null` for that key.
"""
    raw = query_ollama(prompt)
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        parsed = {"name": None, "quantity": None}
    return pd.Series(parsed)

def process_csv(file_path):
    """Process CSV file and return parsed data as list of dicts."""
    # Load CSV as DataFrame
    df = pd.read_csv(file_path)
    results = []

    for _, row in df.iterrows():
        parsed = parse_row_with_llm(row)
        results.append({"name": parsed["name"], "quantity": parsed["quantity"]})

    return results
