
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from cloud.database_service import get_db
from backend.models.url_submission import UrlSubmission
from backend.schemas.url_submission import (
    UrlSubmissionCreate,
    UrlSubmissionOut,
)

router = APIRouter(
    prefix="/api/url-submissions",
    tags=["URL Submissions"],
)


@router.post("/", response_model=UrlSubmissionOut, status_code=201)
def create_url_submission(
    payload: UrlSubmissionCreate,
    db: Session = Depends(get_db),
):
    student_name = payload.student_name.strip()
    registration_number = payload.registration_number.strip()
    assignment_title = payload.assignment_title.strip()

    if not student_name:
        raise HTTPException(status_code=422, detail="Student name is required.")

    if not registration_number:
        raise HTTPException(
            status_code=422,
            detail="Registration number is required.",
        )

    if not assignment_title:
        raise HTTPException(
            status_code=422,
            detail="Assignment title is required.",
        )

    submission = UrlSubmission(
        student_name=student_name,
        registration_number=registration_number,
        assignment_title=assignment_title,
        submission_url=str(payload.submission_url),
    )

    db.add(submission)
    db.commit()
    db.refresh(submission)

    return submission


@router.get("/", response_model=list[UrlSubmissionOut])
def get_url_submissions(db: Session = Depends(get_db)):
    return (
        db.query(UrlSubmission)
        .order_by(UrlSubmission.id.desc())
        .all()
    )
