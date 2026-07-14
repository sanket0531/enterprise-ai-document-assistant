"""initial schema

Revision ID: aeacf2d86ceb
Revises:
Create Date: 2026-07-14 11:54:45.656820
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "aeacf2d86ceb"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # -----------------------------
    # Users Table
    # -----------------------------
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("full_name", sa.String(length=150), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column(
            "role",
            sa.Enum("ADMIN", "EDITOR", "VIEWER", name="userrole"),
            nullable=False,
        ),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("is_verified", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )

    op.create_index(
        "ix_users_email",
        "users",
        ["email"],
        unique=True,
    )

    # -----------------------------
    # Documents Table
    # -----------------------------
    op.create_table(
        "documents",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("filename", sa.String(length=255), nullable=False),
        sa.Column("original_filename", sa.String(length=255), nullable=False),
        sa.Column("file_path", sa.String(length=500), nullable=False),
        sa.Column("file_size", sa.BigInteger(), nullable=False),
        sa.Column("mime_type", sa.String(length=100), nullable=False),
        sa.Column("file_extension", sa.String(length=20), nullable=False),
        sa.Column(
            "status",
            sa.Enum("ACTIVE", "DELETED", name="documentstatus"),
            nullable=False,
        ),
        sa.Column(
            "processing_status",
            sa.Enum(
                "UPLOADED",
                "PROCESSING",
                "CHUNKED",
                "EMBEDDED",
                "INDEXED",
                "READY",
                "FAILED",
                name="processingstatus",
            ),
            nullable=False,
        ),
        sa.Column(
            "uploaded_by",
            sa.Integer(),
            sa.ForeignKey("users.id"),
            nullable=False,
        ),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.UniqueConstraint("filename"),
    )

    # -----------------------------
    # Documents Indexes
    # -----------------------------
    op.create_index(
        "ix_documents_id",
        "documents",
        ["id"],
        unique=False,
    )

    op.create_index(
        "ix_documents_uploaded_by",
        "documents",
        ["uploaded_by"],
        unique=False,
    )

    op.create_index(
        "ix_documents_processing_status",
        "documents",
        ["processing_status"],
        unique=False,
    )

    op.create_index(
        "ix_documents_status",
        "documents",
        ["status"],
        unique=False,
    )

    op.create_index(
        "ix_documents_created_at",
        "documents",
        ["created_at"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""

    # -----------------------------
    # Drop Documents Indexes
    # -----------------------------
    op.drop_index("ix_documents_created_at", table_name="documents")
    op.drop_index("ix_documents_status", table_name="documents")
    op.drop_index("ix_documents_processing_status", table_name="documents")
    op.drop_index("ix_documents_uploaded_by", table_name="documents")
    op.drop_index("ix_documents_id", table_name="documents")

    # Drop Documents Table
    op.drop_table("documents")

    # Drop Users Index
    op.drop_index("ix_users_email", table_name="users")

    # Drop Users Table
    op.drop_table("users")