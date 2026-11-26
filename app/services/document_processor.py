from pathlib import Path



def process_document(file_path: str) -> dict:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Document not found: {file_path}")

    extension = path.suffix.lower()

    if extension != ".txt":
        raise ValueError("Only TXT files are supported")

    text = path.read_text(encoding="utf-8")

    return {
        "filename" : path.name,
        "extension": extension,
        "size_bytes": path.stat().st_size,
        "text" : text,
    }