from datetime import datetime

from sqlalchemy import DateTime, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from cloud.database_service import Base


class UrlSubmission(Base):
    __tablename__ = "url_submissions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    student_name: Mapped[str] = mapped_column(String(150), nullable=False)
    registration_number: Mapped[str] = mapped_column(String(50), nullable=False)
    assignment_title: Mapped[str] = mapped_column(String(200), nullable=False)
    submission_url: Mapped[str] = mapped_column(String(2048), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )

    __table_args__ = (
        Index("ix_url_submissions_registration_number", "registration_number"),
    )