"""
list_granite_models.py
----------------------
Lists every IBM Granite chat model available to your watsonx.ai account.

Uses client.foundation_models.ChatModels — a cached_property on the SDK's
FoundationModelsManager that calls get_chat_model_specs() against the live
API and returns a StrEnum whose members are the account's actual chat models.
Granite entries are filtered by checking whether the model ID contains
"granite" (case-insensitive).

Credentials are loaded from the project's .env file (or from real environment
variables if they are already set).

Run:
    python list_granite_models.py
"""

import os
import sys
from dotenv import load_dotenv

# Load .env before accessing os.environ
load_dotenv()

# ---------------------------------------------------------------------------
# Read credentials — fail early with a clear message if anything is missing
# ---------------------------------------------------------------------------
WATSONX_URL = os.environ.get("WATSONX_URL")
WATSONX_API_KEY = os.environ.get("WATSONX_API_KEY")

missing = [name for name, val in [
    ("WATSONX_URL", WATSONX_URL),
    ("WATSONX_API_KEY", WATSONX_API_KEY),
] if not val]

if missing:
    print(
        f"Error: the following environment variable(s) are not set: "
        f"{', '.join(missing)}\n"
        "Copy .env.example to .env and fill in your IBM watsonx.ai credentials."
    )
    sys.exit(1)

# ---------------------------------------------------------------------------
# Connect to IBM watsonx.ai
# ---------------------------------------------------------------------------
try:
    from ibm_watsonx_ai import APIClient, Credentials

    credentials = Credentials(
        url=WATSONX_URL,
        api_key=WATSONX_API_KEY,
    )
    client = APIClient(credentials)

except Exception as exc:
    print(f"Error: could not connect to IBM watsonx.ai.\n{exc}")
    sys.exit(1)

# ---------------------------------------------------------------------------
# Retrieve chat models via client.foundation_models.ChatModels
#
# ChatModels is a cached_property on FoundationModelsManager.
# Accessing it triggers a live API call to get_chat_model_specs() and
# returns a StrEnum populated with every chat model available to the account.
# Each enum member's .value is the exact model ID string.
# ---------------------------------------------------------------------------
try:
    chat_models_enum = client.foundation_models.ChatModels
except Exception as exc:
    print(f"Error: failed to retrieve chat model list from IBM watsonx.ai.\n{exc}")
    sys.exit(1)

# ---------------------------------------------------------------------------
# Filter for Granite and display results
# ---------------------------------------------------------------------------
granite_models = [
    member.value
    for member in chat_models_enum
    if "granite" in member.value.lower()
]

if granite_models:
    print(
        f"Granite chat models available on your watsonx.ai account "
        f"({len(granite_models)} found):\n"
    )
    for model_id in sorted(granite_models):
        print(f"  {model_id}")
    print()
    print("-- All chat models (client.foundation_models.ChatModels.show()) --")
    chat_models_enum.show()
else:
    print(
        "No Granite chat models were found for your account.\n"
        "This may mean your region or plan does not include Granite chat models.\n"
        "Check your WATSONX_URL and project access, or try a different region endpoint."
    )
