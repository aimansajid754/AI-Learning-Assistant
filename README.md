# AI Learning Assistant Using Gemini API

A Streamlit app that converts PDFs into summaries, multiple choice quizzes, and flashcards using the Gemini API. Optimized to work well on limited free-tier API quotas.

## Features

- Upload a PDF and extract text.
- Generate section summaries, MCQs, and flashcards from each section.
- Export results as downloadable files (.txt and .csv).

## Quickstart

1. Clone or copy the repository to your machine.
2. Create a virtual environment and activate it.

```bash
python -m venv venv
# on macOS / Linux
source venv/bin/activate
# on Windows (PowerShell)
venv\Scripts\Activate.ps1
```

3. Install dependencies.

```bash
pip install -r requirements.txt
```

4. Create an `.env` file at the project root and add your Gemini API key using the name `GEMINI_API_KEY`.

```bash
# .env (do not commit this file)
GEMINI_API_KEY=your_real_api_key_here
```

5. Run the app with Streamlit.

```bash
streamlit run app.py
```

6. Open `http://localhost:8501` in your browser.



