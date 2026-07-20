from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.ai.vectorstore.vector_service import VectorService
from app.core.logger import get_logger
from app.models.document import Document
from app.repositories.document_repository import DocumentRepository
from app.services.chunk_service import ChunkService
from app.services.embedding_service import EmbeddingService
from app.services.extraction_service import ExtractionService
from app.utils.file_storage import FileStorage
from app.utils.file_validator import FileValidator

logger = get_logger(__name__)


class DocumentService:
    """
    Service responsible for document upload and AI processing.
    """

    def __init__(self, db: Session):
        self.repository = DocumentRepository(db)

        # AI Services
        self.extraction_service = ExtractionService()
        self.chunk_service = ChunkService()
        self.embedding_service = EmbeddingService()
        self.vector_service = VectorService()

    async def upload_document(
        self,
        file: UploadFile,
        uploaded_by: int,
    ) -> Document:
        """
        Upload a document, extract text, generate embeddings,
        and index the document into ChromaDB.
        """

        # Validate uploaded file
        await FileValidator.validate(file)

        # Save file
        filename, file_path = await FileStorage.save(file)

        # Extract text
        extracted_text = self.extraction_service.extract_text(file_path)

        logger.info(
            "Successfully extracted %d characters from %s",
            len(extracted_text),
            filename,
        )

        # Create document metadata
        file_extension = (
            file.filename.rsplit(".", 1)[-1].lower()
            if "." in file.filename
            else ""
        )

        document = Document(
            filename=filename,
            original_filename=file.filename,
            file_path=file_path,
            file_size=file.size or 0,
            mime_type=file.content_type or "",
            file_extension=file_extension,
            uploaded_by=uploaded_by,
        )

        # Save metadata into MSSQL
        # document.id becomes available here
        document = self.repository.create(document)

        logger.info(
            "Document metadata saved with ID %s",
            document.id,
        )

        # Create chunks
        chunks = self.chunk_service.create_chunks(extracted_text)

        logger.info(
            "Generated %d chunks",
            len(chunks),
        )

        # Generate embeddings
        embeddings = self.embedding_service.generate_embeddings(chunks)

        logger.info(
            "Generated %d embeddings",
            len(embeddings),
        )

        # Build metadata for every chunk
        metadata = self._build_metadata(
            document=document,
            chunks=chunks,
        )

        # Store vectors into ChromaDB
        try:
            self.vector_service.store_document_vectors(
                document_id=document.id,
                chunks=chunks,
                embeddings=embeddings,
                metadata=metadata,
            )

            logger.info(
                "Successfully indexed document %s into ChromaDB",
                document.id,
            )

        except Exception:
            logger.exception(
                "Failed to index document %s",
                document.id,
            )
            raise

        return document

    def _build_metadata(
        self,
        document: Document,
        chunks: list[str],
    ) -> list[dict]:
        """
        Build metadata for each document chunk.
        """

        return [
            {
                "document_id": str(document.id),
                "chunk_index": index,
                "filename": document.original_filename,
                "uploaded_by": str(document.uploaded_by),
                "file_extension": document.file_extension,
                "mime_type": document.mime_type,
            }
            for index in range(len(chunks))
        ]

    def get_document(
        self,
        document_id: int,
    ) -> Document | None:
        return self.repository.get_by_id(document_id)

    def get_all_documents(self) -> list[Document]:
        return self.repository.get_all()

    def delete_document(
        self,
        document: Document,
    ) -> None:
        self.repository.delete(document)