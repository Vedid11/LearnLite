# LearnLite 📚

**Your Personal AI Learning Assistant**

> LearnLite is an AI-powered learning assistant that transforms complex academic
> content into personalised explanations, key concepts, examples, summaries and
> quizzes using IBM Granite.

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-red)](https://streamlit.io/)
[![IBM watsonx.ai](https://img.shields.io/badge/IBM-watsonx.ai-0530ad)](https://www.ibm.com/products/watsonx-ai)

---

## Overview

Students and self-learners often hit a wall when encountering dense academic
text — whether it is a research paper, a textbook chapter, or lecture notes
written for an expert audience. LearnLite solves this by breaking any academic
content down into five structured outputs, each adapted to the reader's own
knowledge level.

You paste your text, choose how much background you already have
(Beginner → Expert), and IBM Granite delivers a tailored explanation, defined
key terms, relatable examples, a concise summary, and quiz questions — all in
one request.

---

## Features

| Feature | Description |
|---|---|
| **Four learning levels** | Beginner · Intermediate · Advanced · Expert — each produces a distinctly different depth and vocabulary |
| **Simplified explanation** | Plain-language walkthrough adapted to the chosen level |
| **Key terms** | Definitions for the most important technical vocabulary in the text |
| **Relatable examples** | 2–3 concrete, real-world illustrations of the core ideas |
| **Summary** | 3–5 sentence recap of the main points |
| **Quiz** | 3 questions with answers to test and reinforce understanding |

---

## How It Works

```
User pastes academic text
        │
        ▼
LearnLite builds a structured prompt
(system role + level descriptor + section instructions)
        │
        ▼
IBM Granite (ibm/granite-4-h-small) via IBM watsonx.ai
        │
        ▼
Raw response is parsed into five named sections
        │
        ▼
Results displayed across five labelled tabs in the browser
```

1. **`prompts.py`** constructs the chat messages list. It contains level
   descriptors that tell Granite exactly what vocabulary and depth to use, and
   section headings that the response parser later splits on.
2. **`granite_client.py`** resolves credentials (from Streamlit secrets or a
   local `.env` file), initialises `ModelInference`, and calls `model.chat()`.
3. **`app.py`** is the Streamlit interface. It renders the input controls,
   calls the client, parses the response, and displays results in tabs.

---

## IBM Granite & watsonx.ai Integration

LearnLite uses **IBM Granite** — IBM's enterprise-grade foundation model family
— accessed through the official **IBM watsonx.ai Python SDK**
(`ibm-watsonx-ai`).

- Model: `ibm/granite-4-h-small` (configurable via `WATSONX_MODEL_ID`)
- API: `ModelInference.chat()` — the standard chat completions interface
- Authentication: IBM Cloud IAM API key
- No prompt caching, no fine-tuning, no third-party AI providers

---

## Architecture

```
LearnLite/
├── app.py                  # Streamlit UI — page config, layout, result tabs
├── granite_client.py       # watsonx.ai SDK wrapper — credential resolution, chat call
├── prompts.py              # Prompt engineering — level descriptors, section headings
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variable template (no real values)
├── .gitignore              # Excludes .env, secrets.toml, venv, caches
├── .streamlit/
│   └── secrets.toml.example  # Streamlit secrets template (no real values)
├── check_granite.py        # Development utility: test the IBM Granite connection
└── list_granite_models.py  # Development utility: list available Granite model IDs
```

---

## Prerequisites

- Python 3.9 or later
- An [IBM Cloud account](https://cloud.ibm.com/) with access to **IBM watsonx.ai**
- A watsonx.ai **project ID**
- An IBM Cloud **API key**
- A Granite model ID available in your account (e.g. `ibm/granite-4-h-small`)

---

## Local Installation

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/LearnLite.git
cd LearnLite
```

### 2. Create and activate a virtual environment

```powershell
# Windows (PowerShell)
python -m venv venv
venv\Scripts\activate
```

```bash
# macOS / Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure credentials

```powershell
# Windows
copy .env.example .env
```

```bash
# macOS / Linux
cp .env.example .env
```

Open `.env` and fill in your IBM watsonx.ai credentials:

```env
WATSONX_API_KEY=<your IBM Cloud API key>
WATSONX_PROJECT_ID=<your watsonx.ai project ID>
WATSONX_URL=https://us-south.ml.cloud.ibm.com
WATSONX_MODEL_ID=ibm/granite-4-h-small
```

> **Security:** `.env` is in `.gitignore` and is never committed to version
> control. Never share or hardcode credentials.

#### Where to find each value

| Variable | Location |
|---|---|
| `WATSONX_API_KEY` | IBM Cloud → Manage → Access (IAM) → API keys |
| `WATSONX_PROJECT_ID` | watsonx.ai → Your project → Manage → General → Project ID |
| `WATSONX_URL` | Regional endpoint, e.g. `https://us-south.ml.cloud.ibm.com` |
| `WATSONX_MODEL_ID` | Run `python list_granite_models.py` to list available IDs |

### 5. Run the application

```bash
streamlit run app.py
```

Streamlit opens **http://localhost:8501** automatically.

---

## Deploying to Streamlit Community Cloud

### 1. Push your code to GitHub

Ensure `.env` and `.streamlit/secrets.toml` are in `.gitignore` (they already
are) and are **not** present in the repository.

### 2. Connect to Streamlit Community Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
2. Click **New app**.
3. Select your repository, branch (`main`), and set **Main file path** to `app.py`.

### 3. Add secrets

Before clicking **Deploy**, open **Advanced settings → Secrets** and paste:

```toml
WATSONX_API_KEY    = "your_ibm_cloud_api_key_here"
WATSONX_PROJECT_ID = "your_watsonx_project_id_here"
WATSONX_URL        = "https://us-south.ml.cloud.ibm.com"
WATSONX_MODEL_ID   = "ibm/granite-4-h-small"
```

Streamlit stores these securely — they are never visible in source code or
repository history.

### 4. Deploy

Click **Deploy**. Streamlit Community Cloud installs `requirements.txt` and
starts the app automatically.

### How credential resolution works

`granite_client.py` checks two sources in order:

1. **`st.secrets`** — used automatically on Streamlit Community Cloud.
2. **Environment variables / `.env`** — used for local development.

No code change is needed when switching between environments.

---

## Usage

1. Paste any academic text into the **Academic Content** text area.
2. Select a **Learning Level**: Beginner, Intermediate, Advanced, or Expert.
3. Click **✨ Simplify Content**.
4. Wait for IBM Granite to generate the response (a spinner is shown).
5. Browse the five output tabs:
   - **💡 Explanation** — level-adapted simplified explanation
   - **📖 Key Terms** — defined technical vocabulary
   - **🔗 Examples** — relatable real-world illustrations
   - **📝 Summary** — short recap paragraph
   - **❓ Quiz** — 3 questions with answers
6. Click **🗑️ Clear** to reset and start again.

---

## Technologies Used

| Layer | Technology |
|---|---|
| Frontend | [Streamlit](https://streamlit.io/) |
| AI model | [IBM Granite](https://www.ibm.com/granite) (via `WATSONX_MODEL_ID`) |
| AI platform | [IBM watsonx.ai](https://www.ibm.com/products/watsonx-ai) |
| SDK | [ibm-watsonx-ai](https://pypi.org/project/ibm-watsonx-ai/) |
| Language | Python 3.9+ |

---

## Development Utilities

These scripts are for development and testing only and are not part of the
deployed application.

### Test the IBM Granite connection

```bash
python check_granite.py
```

Sends a single test message to IBM Granite and prints the response. Useful for
verifying credentials before running the full app.

### List available Granite models

```bash
python list_granite_models.py
```

Queries your watsonx.ai account and prints every Granite chat model ID
available to you. Use the output to set `WATSONX_MODEL_ID`.

---

## Future Improvements

- **Conversation memory** — allow follow-up questions on the same text
- **File upload** — accept PDF and DOCX files in addition to pasted text
- **Export** — download the full explanation set as a PDF or Markdown file
- **History** — save and revisit previous explanations within a session
- **Additional languages** — generate explanations in languages other than English
- **Accessibility** — screen-reader friendly result rendering

---

## License

MIT License — see [LICENSE](LICENSE) for details.
