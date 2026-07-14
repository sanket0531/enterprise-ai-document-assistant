from fastapi import HTTPException, UploadFile, status


class FileValidator:
    ALLOWED_EXTENSIONS = {
        "pdf",
        "docx",
        "txt",
        "md",
    }

    MAX_FILE_SIZE = 20 * 1024 * 1024  # 20 MB

    @classmethod
    async def validate(cls, file: UploadFile) -> None:
        if not file.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Filename is required.",
            )

        extension = file.filename.rsplit(".", 1)[-1].lower()

        if extension not in cls.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported file type. Allowed: {', '.join(cls.ALLOWED_EXTENSIONS)}",
            )

        content = await file.read()
        file_size = len(content)

        if file_size == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uploaded file is empty.",
            )

        if file_size > cls.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File size exceeds the 20 MB limit.",
            )

        # Reset file pointer so the file can be read again later
        await file.seek(0)