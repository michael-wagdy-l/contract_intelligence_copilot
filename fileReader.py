import io

from pypdf import PdfReader

def read_file_as_text(file_bytes: bytes, filename: str) -> str:
    
    if filename.endswith(".pdf"):
        reader = PdfReader(io.BytesIO(file_bytes))
        pages = [page.extract_text() or "" for page in reader.pages]
        return "\n".join(pages)

    else:
        try:
            return file_bytes.decode("utf-8")
        except UnicodeDecodeError:
            return file_bytes.decode("windows-1252")