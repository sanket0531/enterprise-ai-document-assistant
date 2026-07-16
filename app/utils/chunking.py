from langchain_text_splitters import RecursiveCharacterTextSplitter


class TextChunker:
    """
    Utility class responsible for splitting extracted text
    into smaller chunks for RAG.
    """

    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ) -> None:
        self._text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            is_separator_regex=False,
        )

    def split_text(self, text: str) -> list[str]:
        """
        Split extracted text into chunks.

        Args:
            text: Extracted document text.

        Returns:
            List of text chunks.
        """
        if not text or not text.strip():
            return []

        return self._text_splitter.split_text(text)