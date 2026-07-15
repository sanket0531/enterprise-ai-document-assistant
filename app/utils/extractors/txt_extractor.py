from app.utils.extractors.base_extractor import BaseExtractor


class TXTExtractor(BaseExtractor):
    """
    Extract text from plain text (.txt) files.
    """

    def extract(self, file_path: str) -> str:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read().strip()