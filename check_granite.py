"""
check_granite.py
----------------
Sends a test chat message to IBM Granite via watsonx.ai and prints
the assistant's response.

Reads four environment variables from .env:
  WATSONX_API_KEY      - IBM Cloud IAM API key
  WATSONX_PROJECT_ID   - watsonx.ai project ID
  WATSONX_URL          - Regional endpoint URL
  WATSONX_MODEL_ID     - Granite model ID to test

Run:
    python check_granite.py
"""

import os
import sys
from dotenv import load_dotenv

# Load .env before reading os.environ
load_dotenv()

# ---------------------------------------------------------------------------
# Read and validate credentials
# ---------------------------------------------------------------------------
WATSONX_API_KEY    = os.environ.get("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.environ.get("WATSONX_PROJECT_ID")
WATSONX_URL        = os.environ.get("WATSONX_URL")
WATSONX_MODEL_ID   = os.environ.get("WATSONX_MODEL_ID")

missing = [
    name for name, val in [
        ("WATSONX_API_KEY",    WATSONX_API_KEY),
        ("WATSONX_PROJECT_ID", WATSONX_PROJECT_ID),
        ("WATSONX_URL",        WATSONX_URL),
        ("WATSONX_MODEL_ID",   WATSONX_MODEL_ID),
    ]
    if not val
]

if missing:
    print(
        f"Error: the following environment variable(s) are not set: "
        f"{', '.join(missing)}\n"
        "Add them to your .env file and try again.\n"
        "See .env.example for the required variable names."
    )
    sys.exit(1)

# ---------------------------------------------------------------------------
# Initialise ModelInference
# ---------------------------------------------------------------------------
try:
    from ibm_watsonx_ai import Credentials
    from ibm_watsonx_ai.foundation_models import ModelInference

    credentials = Credentials(
        url=WATSONX_URL,
        api_key=WATSONX_API_KEY,
    )

    model = ModelInference(
        model_id=WATSONX_MODEL_ID,
        credentials=credentials,
        project_id=WATSONX_PROJECT_ID,
    )

except Exception as exc:
    print(f"Error: could not initialise IBM Granite model.\n{exc}")
    sys.exit(1)

# ---------------------------------------------------------------------------
# Test conversation
# ---------------------------------------------------------------------------
messages = [
    {
        "role": "system",
        "content": "You are a helpful educational assistant.",
    },
    {
        "role": "user",
        "content": "Explain photosynthesis in three simple sentences for a beginner.",
    },
]

print(f"Model : {WATSONX_MODEL_ID}")
print(f"URL   : {WATSONX_URL}")
print("-" * 60)
print("Sending test message to IBM Granite...\n")

# ---------------------------------------------------------------------------
# Call model.chat() and extract the assistant's reply
# ---------------------------------------------------------------------------
try:
    response = model.chat(messages=messages)
    reply = response["choices"][0]["message"]["content"]
except Exception as exc:
    print(f"Error: the chat request failed.\n{exc}")
    sys.exit(1)

print("Assistant response:")
print("-" * 60)
print(reply)
