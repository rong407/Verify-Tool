import json

def extract_from_txt(file_path):
    with open(file_path, "r", errors="ignore") as f:
        data = f.read()

    if "FP:" in data:
        raw = data.split("FP:")[-1]
        return raw.strip()

    return None


def extract_from_pdf(file_path):
    try:
        import fitz
        doc = fitz.open(file_path)
        meta = doc.metadata
        return meta.get("subject", None)
    except:
        return None


def extract_from_docx(file_path):
    try:
        from docx import Document
        doc = Document(file_path)
        return doc.core_properties.comments
    except:
        return None


def extract_fingerprint(file_path):

    ext = file_path.split(".")[-1].lower()

    if ext == "txt":
        return extract_from_txt(file_path)

    elif ext == "pdf":
        return extract_from_pdf(file_path)

    elif ext == "docx":
        return extract_from_docx(file_path)

    else:
        return None
