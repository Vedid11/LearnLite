"""
granite_client.py
-----------------
Handles all communication with IBM watsonx.ai using the chat API.

Credential resolution order (first source that has all four values wins):
  1. Streamlit secrets  (st.secrets)  — used on Streamlit Community Cloud
  2. Environment variables / .env     — used for local development

Required keys:
  WATSONX_API_KEY      - IBM Cloud IAM API key
  WATSONX_PROJECT_ID   - watsonx.ai project ID
  WATSONX_URL          - Regional endpoint, e.g. https://us-south.ml.cloud.ibm.com
  WATSONX_MODEL_ID     - Granite model ID, e.g. ibm/granite-4-h-small

Never hardcode or expose these values in source code.
"""

import os

# Load .env for local development.
# python-dotenv is a no-op when .env does not exist (safe on Streamlit Cloud).
from dotenv import load_dotenv
load_dotenv()

from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference

# Keys required for the IBM watsonx.ai connection.
_REQUIRED_KEYS = (
    "WATSONX_API_KEY",
    "WATSONX_PROJECT_ID",
    "WATSONX_URL",
    "WATSONX_MODEL_ID",
)


def _get_credentials() -> dict:
    """
    Resolve credentials from st.secrets (Streamlit Cloud) or os.environ (.env).

    Resolution order
    ----------------
    1. If Streamlit is running and st.secrets contains all four keys, use them.
    2. Otherwise fall back to environment variables (populated by .env locally
       or by the host environment in any other deployment).

    Raises EnvironmentError listing every missing key if neither source is
    complete.
    """
    # --- Try st.secrets first (Streamlit Community Cloud) -------------------
    try:
        import streamlit as st
        secrets = st.secrets
        if all(key in secrets for key in _REQUIRED_KEYS):
            return {key: secrets[key] for key in _REQUIRED_KEYS}
    except Exception:
        # st.secrets raises outside a Streamlit session (e.g. unit tests,
        # standalone scripts). Fall through to env vars.
        pass

    # --- Fall back to environment variables / .env --------------------------
    creds = {key: os.environ.get(key) for key in _REQUIRED_KEYS}
    missing = [key for key, val in creds.items() if not val]
    if missing:
        raise EnvironmentError(
            f"Missing credential(s): {', '.join(missing)}. "
            "For local development: copy .env.example to .env and fill in your values. "
            "For Streamlit Cloud: add the keys to the app's Secrets settings."
        )
    return creds


def chat_completion(messages: list, return_usage: bool = False):
    """
    Send a list of chat messages to IBM Granite and return the result.

    Parameters
    ----------
    messages     : list of dicts with "role" and "content" keys,
                   e.g. [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}]
    return_usage : When False (default) returns only the generated text string,
                   preserving backward compatibility.
                   When True returns a tuple (text, usage) where usage is a dict:
                     {
                       "prompt_tokens"     : int | None,
                       "completion_tokens" : int | None,
                       "total_tokens"      : int | None,
                     }
                   All three values are taken directly from the API response's
                   "usage" object (fields: prompt_tokens, completion_tokens,
                   total_tokens). If the field is absent, its value is None.

    Returns
    -------
    str                    — when return_usage is False
    tuple[str, dict]       — when return_usage is True

    Raises
    ------
    EnvironmentError : If any required credential is missing from both sources.
    RuntimeError     : If the IBM watsonx.ai API call fails.
    """
    creds = _get_credentials()

    credentials = Credentials(
        url=creds["WATSONX_URL"],
        api_key=creds["WATSONX_API_KEY"],
    )

    model = ModelInference(
        model_id=creds["WATSONX_MODEL_ID"],
        credentials=credentials,
        project_id=creds["WATSONX_PROJECT_ID"],
    )

    try:
        response = model.chat(messages=messages)
        text = response["choices"][0]["message"]["content"]

        if not return_usage:
            return text

        # Extract usage from the top-level "usage" key.
        # Confirmed field names from live API response (SDK 1.9.1):
        #   prompt_tokens, completion_tokens, total_tokens
        raw_usage = response.get("usage") or {}
        usage = {
            "prompt_tokens":     raw_usage.get("prompt_tokens"),
            "completion_tokens": raw_usage.get("completion_tokens"),
            "total_tokens":      raw_usage.get("total_tokens"),
        }
        return text, usage

    except Exception as exc:
        raise RuntimeError(
            f"IBM watsonx.ai chat request failed: {exc}"
        ) from exc
