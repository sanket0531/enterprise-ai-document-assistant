import fitz  # PyMuPDF

from app.utils.extractors.base_extractor import BaseExtractor


class PDFExtractor(BaseExtractor):
    """
    Extract text from PDF documents using PyMuPDF.
    """

    def extract(self, file_path: str) -> str:
        text = []

        with fitz.open(file_path) as pdf:
            for page in pdf:
                page_text = page.get_text("text")
                if page_text:
                    text.append(page_text)

        return "\n".join(text).strip()