"""
prompts.py
----------
Builds the chat messages list sent to IBM Granite.
Keeps all AI instructions separate from the UI and client code.
"""

# ---------------------------------------------------------------------------
# Level descriptors
# Describes what Granite should assume about the reader at each level.
# ---------------------------------------------------------------------------
LEVEL_DESCRIPTORS = {
    "Beginner": (
        "The student has no prior knowledge of the subject. "
        "Use very simple everyday language, short sentences, and basic analogies. "
        "Avoid all jargon. Explain as if talking to a curious 12-year-old."
    ),
    "Intermediate": (
        "The student has basic familiarity with the subject. "
        "Use clear language with some domain vocabulary, but explain every technical term. "
        "Use relatable real-world examples."
    ),
    "Advanced": (
        "The student has solid subject knowledge. "
        "Use accurate technical language, assume familiarity with core concepts, "
        "and focus on nuance, edge cases, and deeper understanding."
    ),
    "Expert": (
        "The student is a domain expert or graduate-level learner. "
        "Use full technical vocabulary, precise definitions, and sophisticated examples. "
        "Highlight subtleties, trade-offs, and connections to related advanced topics."
    ),
}

# ---------------------------------------------------------------------------
# Section headings
# The parser in app.py splits on these exact strings.
# If you change them here, update the parser accordingly.
# ---------------------------------------------------------------------------
SECTION_HEADINGS = {
    "explanation": "## Simplified Explanation",
    "key_terms":   "## Key Terms",
    "examples":    "## Relatable Examples",
    "summary":     "## Summary",
    "quiz":        "## Quiz Questions",
}


def build_messages(text: str, level: str) -> list:
    """
    Return a chat messages list for IBM Granite's chat API.

    Parameters
    ----------
    text  : The academic content the student wants simplified.
    level : One of Beginner | Intermediate | Advanced | Expert.

    Returns
    -------
    list of dicts with "role" and "content" keys, ready for model.chat().
    """
    level_desc = LEVEL_DESCRIPTORS.get(level, LEVEL_DESCRIPTORS["Beginner"])
    h = SECTION_HEADINGS

    system_content = (
        "You are an expert educational assistant helping students understand academic content. "
        f"The student's level is: {level}. "
        f"Level guidance: {level_desc} "
        "Always respond with exactly five sections using the headings below. "
        "Do not add, rename, or reorder the headings. "
        "Do not add any text before the first heading."
    )

    user_content = f"""Process the academic text below and return EXACTLY these five sections:

{h['explanation']}
Write a clear, thorough explanation adapted to the student's level.

{h['key_terms']}
List the most important technical terms with concise, level-appropriate definitions.
Format each as: **Term**: Definition

{h['examples']}
Give 2-3 relatable, concrete examples that illustrate the main ideas.

{h['summary']}
Write a short paragraph (3-5 sentences) summarising the key points.

{h['quiz']}
Write exactly 3 quiz questions that test understanding. Provide the answer immediately after each question.
Format:
Q1: <question>
A1: <answer>

Q2: <question>
A2: <answer>

Q3: <question>
A3: <answer>

---
Academic text:
{text}"""

    return [
        {"role": "system", "content": system_content},
        {"role": "user",   "content": user_content},
    ]
