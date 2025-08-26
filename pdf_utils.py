import pdfplumber

def extract_text_from_pdf(file_path: str) -> str:
    text_parts = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            t = page.extract_text() or ""
            text_parts.append(t.strip())
    full_text = "\n".join(text_parts)
    # basic cleanup
    full_text = "\n".join([line for line in full_text.splitlines() if line.strip()])
    return full_text

def chunk_text(text: str, max_chars: int = 7000, overlap: int = 500):
    """Rough chunking by characters to stay within model limits."""
    chunks = []
    start = 0
    n = len(text)
    while start < n:
        end = min(start + max_chars, n)
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap
        if start < 0:
            start = 0
    return chunks
