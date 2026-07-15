from docx import Document

from app.utils.extractors.base_extractor import BaseExtractor


class DOCXExtractor(BaseExtractor):
    """
    Extract text from Microsoft Word (.docx) documents.
    """

    def extract(self, file_path: str) -> str:
        document = Document(file_path)

        text = [
            paragraph.text.strip()
            for paragraph in document.paragraphs
            if paragraph.text.strip()
        ]

        return "\n".join(text)