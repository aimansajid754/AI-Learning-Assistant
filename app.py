import os
import json
import time
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from pdf_utils import extract_text_from_pdf, chunk_text
from ai import summarize_section, generate_mcqs, generate_flashcards

load_dotenv()

# ------------------ Defaults for speed ------------------
CHUNK_SIZE = 4000   # small chunks = faster
OVERLAP = 0         # no duplication

# ------------------ Streamlit Page Setup ------------------
st.set_page_config(page_title="Personalized Learning Assistant", layout="wide")
st.title("📘 Personalized Learning Assistant")
st.markdown(
    "Upload a PDF and get **summaries, quizzes, or flashcards**. "
    "Optimized for the free Gemini API tier (slower but avoids quota errors)."
)

# ------------------ Sidebar ------------------
with st.sidebar:
    st.header("⚙️ Settings")

    # User chooses what to generate
    generate_summaries = st.checkbox("Generate Summaries", value=True)
    generate_mcq = st.checkbox("Generate Quizzes", value=False)
    generate_flash = st.checkbox("Generate Flashcards", value=False)

    style = st.radio("Summary style", ["Concise", "Detailed"], index=0).lower()
    difficulty = st.radio("MCQ difficulty", ["Easy", "Medium", "Hard"], index=1).lower()

    n_mcq = st.number_input("MCQs per section", 4, 12, 6, step=1)
    n_cards = st.number_input("Flashcards per section", 4, 12, 8, step=1)

    st.markdown("---")
    uploaded = st.file_uploader("📂 Upload a PDF", type=["pdf"])

# ------------------ Processing Logic ------------------
def process_chunk(ch, idx, style, n_mcq, difficulty, n_cards):
    """Run selected AI tasks for one chunk"""
    result = {"section": idx}

    if generate_summaries:
        result["summary"] = summarize_section(ch, style)
    if generate_mcq:
        result["mcqs"] = [
            {**q, "section": idx}
            for q in generate_mcqs(ch, n_questions=n_mcq, difficulty=difficulty)
        ]
    if generate_flash:
        result["flashcards"] = [
            {**c, "section": idx}
            for c in generate_flashcards(ch, n_cards=n_cards)
        ]

    return result

# ------------------ Main App ------------------
tabs = st.tabs(["📑 Summaries", "❓ Quizzes", "🃏 Flashcards", "⬇️ Export"])

if uploaded:
    temp_path = os.path.join("output", "upload.pdf")
    os.makedirs("output", exist_ok=True)
    with open(temp_path, "wb") as f:
        f.write(uploaded.read())

    with st.spinner("🔍 Extracting text..."):
        text = extract_text_from_pdf(temp_path)

    chunks = chunk_text(text, max_chars=CHUNK_SIZE, overlap=OVERLAP)
    st.success(f"✅ Extracted text. Split into {len(chunks)} sections.")

    # Sequential processing (to avoid quota spikes)
    results = []
    for i, ch in enumerate(chunks, 1):
        with st.spinner(f"⚡ Processing section {i}..."):
            results.append(process_chunk(ch, i, style, n_mcq, difficulty, n_cards))
            time.sleep(5)  # space requests out to stay under free-tier quota

    # Store in session state
    if generate_summaries:
        st.session_state["summaries"] = [
            {"section": r["section"], "summary": r["summary"]} for r in results if "summary" in r
        ]
    if generate_mcq:
        st.session_state["mcqs"] = pd.DataFrame(
            [q for r in results if "mcqs" in r for q in r["mcqs"]]
        )
    if generate_flash:
        st.session_state["flashcards"] = pd.DataFrame(
            [c for r in results if "flashcards" in r for c in r["flashcards"]]
        )

    # ------------------ Summaries Tab ------------------
    with tabs[0]:
        st.subheader("📑 Section Summaries")
        if "summaries" in st.session_state:
            for s in st.session_state["summaries"]:
                with st.container():
                    st.markdown(f"### Section {s['section']}")
                    st.info(s["summary"])
        else:
            st.info("⚠️ Summaries not generated (enable in sidebar).")

    # ------------------ Quizzes Tab ------------------
    with tabs[1]:
        st.subheader("❓ Generated MCQs")
        if "mcqs" in st.session_state and not st.session_state["mcqs"].empty:
            for _, row in st.session_state["mcqs"].iterrows():
                with st.expander(f"Q{row.name+1} (Section {row['section']})"):
                    st.write(row["question"])
                    options = row["options"] if isinstance(row["options"], list) else json.loads(row["options"])
                    for i, opt in enumerate(options):
                        st.write(f"{chr(65+i)}. {opt}")
                    st.markdown(f"**Answer:** {chr(65 + int(row['answer_index']))}")
                    st.caption(f"Explanation: {row['explanation']}")
        else:
            st.info("⚠️ Quizzes not generated (enable in sidebar).")

    # ------------------ Flashcards Tab ------------------
    with tabs[2]:
        st.subheader("🃏 Flashcards")
        if "flashcards" in st.session_state and not st.session_state["flashcards"].empty:
            for _, row in st.session_state["flashcards"].iterrows():
                with st.container():
                    st.markdown(f"**Q (Section {row['section']}):** {row['q']}")
                    st.success(f"A: {row['a']}")
        else:
            st.info("⚠️ Flashcards not generated (enable in sidebar).")

    # ------------------ Export Tab ------------------
    with tabs[3]:
        st.subheader("⬇️ Export Results")
        if "summaries" in st.session_state:
            summaries_txt = "\n\n".join(
                [f"Section {s['section']}\n{s['summary']}" for s in st.session_state["summaries"]]
            )
            st.download_button("📑 Download summaries (.txt)", summaries_txt, file_name="summaries.txt")

        if "mcqs" in st.session_state:
            csv = st.session_state["mcqs"].to_csv(index=False).encode("utf-8")
            st.download_button("❓ Download MCQs (.csv)", csv, file_name="mcqs.csv")

        if "flashcards" in st.session_state:
            csv2 = st.session_state["flashcards"].to_csv(index=False).encode("utf-8")
            st.download_button("🃏 Download flashcards (.csv)", csv2, file_name="flashcards.csv")
else:
    st.info("📂 Upload a PDF to begin.")
