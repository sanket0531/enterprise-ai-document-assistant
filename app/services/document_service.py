from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.models.document import Document
from app.repositories.document_repository import DocumentRepository
from app.utils.file_storage import FileStorage
from app.utils.file_validator import FileValidator


class DocumentService:
    def __init__(self, db: Session):
        self.repository = DocumentRepository(db)

    async def upload_document(
        self,
        file: UploadFile,
        uploaded_by: int,
    ) -> Document:
        # Validate uploaded file
        await FileValidator.validate(file)

        # Save file to disk
        filename, file_path = await FileStorage.save(file)

        # Create document model
        document = Document(
            filename=filename,
            original_filename=file.filename,
            file_path=file_path,
            file_size=file.size if file.size else 0,
            mime_type=file.content_type or "",
            file_extension=file.filename.rsplit(".", 1)[-1].lower(),
            uploaded_by=uploaded_by,
        )

        # Save metadata
        return self.repository.create(document)

    def get_document(self, document_id: int) -> Document | None:
        return self.repository.get_by_id(document_id)

    def get_all_documents(self) -> list[Document]:
        return self.repository.get_all()

    def delete_document(self, document: Document) -> None:
        self.repository.delete(document)