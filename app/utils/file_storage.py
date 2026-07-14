import os
import shutil
import uuid

from fastapi import UploadFile


class FileStorage:
    UPLOAD_DIRECTORY = "uploads/documents"

    @classmethod
    async def save(cls, file: UploadFile) -> tuple[str, str]:
        """
        Saves the uploaded file and returns:
        (generated_filename, file_path)
        """

        # Create upload directory if it doesn't exist
        os.makedirs(cls.UPLOAD_DIRECTORY, exist_ok=True)

        # Get file extension
        extension = file.filename.rsplit(".", 1)[-1].lower()

        # Generate unique filename
        generated_filename = f"{uuid.uuid4().hex}.{extension}"

        # Full file path
        file_path = os.path.join(
            cls.UPLOAD_DIRECTORY,
            generated_filename
        )

        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return generated_filename, file_path