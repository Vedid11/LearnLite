# LearnLite 📚

**AI-Powered Course Content Simplification Agent**  
Edunet Internship — Problem Statement PS19

---

## Overview

LearnLite helps students understand complex academic content by generating
level-appropriate explanations, key-term definitions, relatable examples,
concise summaries, and quiz questions — all powered by **IBM Granite** through
the official **IBM watsonx.ai Python SDK**.

---

## Features

| Feature | Description |
|---|---|
| Learning levels | Beginner · Intermediate · Advanced · Expert |
| Simplified explanation | Plain-language explanation adapted to the chosen level |
| Key terms | Definitions for important technical vocabulary |
| Relatable examples | 2–3 concrete, real-world illustrations |
| Summary | 3–5 sentence recap of the main points |
| Quiz | 3 questions with answers to test understanding |

---

## Technologies Used

| Layer | Technology |
|---|---|
| Frontend | [Streamlit](https://streamlit.io/) |
| AI model | IBM Granite (configured via `WATSONX_MODEL_ID`) |
| AI platform | [IBM watsonx.ai](https://www.ibm.com/products/watsonx-ai) |
| SDK | [ibm-watsonx-ai](https://pypi.org/project/ibm-watsonx-ai/) |
| Language | Python 3.9+ |
| IDE | IBM Bob |

---

## Project Structure

```
LearnLite/
├── app.py                          # Streamlit web interface
├── granite_client.py               # IBM watsonx.ai SDK wrapper (chat API)
├── prompts.py                      # Chat message builder and level descriptors
├── requirements.txt                # Python dependencies
├── .env.example                    # Env var template (no real values)
├── .gitignore                      # Excludes .env, secrets.toml, venv, caches
├── .streamlit/
│   └── secrets.toml.example        # Streamlit secrets template (no real values)
├── check_granite.py                # One-off connection test (not part of the app)
├── list_granite_models.py          # Lists available Granite models (not part of the app)
└── README.md                       # This file
```

---

## Prerequisites

- Python 3.9 or later
- An [IBM Cloud account](https://cloud.ibm.com/) with access to **IBM watsonx.ai**
- A watsonx.ai **project ID**
- An IBM Cloud **API key**
- A Granite model ID available to your account (e.g. `ibm/granite-4-h-small`)

---

## Local Installation and Running

### 1. Clone or download the project

```bash
git clone <your-repo-url>
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

Open `.env` and fill in all four values:

```
WATSONX_API_KEY=<your IBM Cloud API key>
WATSONX_PROJECT_ID=<your watsonx.ai project ID>
WATSONX_URL=https://us-south.ml.cloud.ibm.com
WATSONX_MODEL_ID=ibm/granite-4-h-small
```

> **Security:** `.env` is listed in `.gitignore` and will never be committed.
> Never share or hardcode credentials.

#### Where to find your credentials

| Variable | Location |
|---|---|
| `WATSONX_API_KEY` | IBM Cloud → Manage → Access (IAM) → API keys |
| `WATSONX_PROJECT_ID` | watsonx.ai → Your project → Manage → General → Project ID |
| `WATSONX_URL` | Use the URL for your region, e.g. `https://us-south.ml.cloud.ibm.com` |
| `WATSONX_MODEL_ID` | Run `python list_granite_models.py` to list available Granite model IDs |

### 5. Run the application

```bash
streamlit run app.py
```

Streamlit will open **http://localhost:8501** in your browser automatically.

---

## Streamlit Community Cloud Deployment

### 1. Push your code to GitHub

Make sure `.env` and `.streamlit/secrets.toml` are listed in `.gitignore` and
are **not** in your repository.

Only these files should be committed:

```
app.py
granite_client.py
prompts.py
requirements.txt
.env.example
.gitignore
.streamlit/secrets.toml.example
README.md
```

### 2. Connect to Streamlit Community Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
2. Click **New app**.
3. Select your repository, branch, and set the **Main file path** to `app.py`.

### 3. Configure Secrets

Before clicking **Deploy**, open **Advanced settings → Secrets** and paste:

```toml
WATSONX_API_KEY    = "your_ibm_cloud_api_key_here"
WATSONX_PROJECT_ID = "your_watsonx_project_id_here"
WATSONX_URL        = "https://us-south.ml.cloud.ibm.com"
WATSONX_MODEL_ID   = "ibm/granite-4-h-small"
```

Replace the placeholder values with your real IBM credentials.
These secrets are stored securely by Streamlit and are never visible in your code or repository.

### 4. Deploy

Click **Deploy**. Streamlit Cloud will install `requirements.txt` automatically and start the app.

### How credential resolution works

`granite_client.py` checks sources in this order:

1. **`st.secrets`** — used automatically on Streamlit Community Cloud.
2. **Environment variables / `.env`** — used for local development.

No code change is needed when switching between environments.

---

## Usage

1. Paste academic text into the **Academic Content** text area.
2. Select your **Learning Level** (Beginner → Expert).
3. Click **✨ Simplify Content**.
4. Wait for IBM Granite to generate the response (a spinner is shown).
5. Browse the results across five tabs:
   - **💡 Explanation** — simplified explanation
   - **📖 Key Terms** — defined technical vocabulary
   - **🔗 Examples** — relatable real-world examples
   - **📝 Summary** — short recap
   - **❓ Quiz** — 3 questions with answers
6. Click **🗑️ Clear** to reset the form.

---

## Utility Scripts

These scripts are for development and testing only — not part of the deployed application.

### Test the IBM Granite connection

```bash
python check_granite.py
```

### List available Granite models

```bash
python list_granite_models.py
```

---

## Restrictions

- IBM Granite via watsonx.ai is the **only** AI provider used.
- No LangChain, Langflow, OpenAI, or Gemini integrations.
- No model training or fine-tuning.
- No credentials are hardcoded anywhere in the source code.
- All AI-generated content comes live from IBM Granite — no fake or hardcoded responses.

---

## License

This project was created for the Edunet Foundation internship programme.
