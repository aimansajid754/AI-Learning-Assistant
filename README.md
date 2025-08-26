# Personalized Learning Assistant

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

## Notes on secrets

- Do not commit `.env` to the repository. Use `.env.example` as a template.
- When deploying on a hosting service or GitHub Actions, store the key in repository secrets and read it from environment variables at runtime.

## Creating the GitHub repo and pushing

Option A: use the GitHub web UI

- Create a new repository on GitHub.
- Follow the instructions to add a remote and push your local branch.

Option B: use the gh CLI (if installed)

```bash
git init
git branch -M main
git add .
git commit -m "Initial commit: Streamlit app"
gh repo create YOUR_USERNAME/personalized-learning-assistant --public --source=. --remote=origin --push
```

Alternative if not using gh:

```bash
git remote add origin git@github.com:YOUR_USERNAME/personalized-learning-assistant.git
git push -u origin main
```

## GitHub Actions - basic CI

See `.github/workflows/python-ci.yml` for a simple workflow that installs requirements and runs a sanity check.
