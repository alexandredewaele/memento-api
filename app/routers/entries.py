from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.database import get_db
from app.models import JournalEntry, EntryCategory, User
from app.schemas import EntryCreate, EntryUpdate, EntryResponse, EntryListResponse
from app.dependencies import get_current_user

router = APIRouter(prefix="/api/entries", tags=["Journal Entries"])


@router.get("", response_model=EntryListResponse)
def list_entries(
    category: Optional[EntryCategory] = Query(None),
    search: Optional[str] = Query(None),
    is_favorite: Optional[bool] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    q = db.query(JournalEntry).filter(JournalEntry.user_id == user.id)
    if category:
        q = q.filter(JournalEntry.category == category)
    if search:
        term = f"%{search}%"
        q = q.filter(or_(JournalEntry.title.ilike(term), JournalEntry.content.ilike(term)))
    if is_favorite is not None:
        q = q.filter(JournalEntry.is_favorite == is_favorite)
    total = q.count()
    entries = q.order_by(JournalEntry.created_at.desc()).offset(skip).limit(limit).all()
    return EntryListResponse(entries=entries, total=total, skip=skip, limit=limit)


@router.get("/{entry_id}", response_model=EntryResponse)
def get_entry(entry_id: UUID, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    entry = db.query(JournalEntry).filter(JournalEntry.id == entry_id, JournalEntry.user_id == user.id).first()
    if not entry:
        raise HTTPException(404, "Entry not found.")
    return entry


@router.post("", response_model=EntryResponse, status_code=201)
def create_entry(data: EntryCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    entry = JournalEntry(user_id=user.id, **data.model_dump())
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


@router.put("/{entry_id}", response_model=EntryResponse)
def update_entry(entry_id: UUID, data: EntryUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    entry = db.query(JournalEntry).filter(JournalEntry.id == entry_id, JournalEntry.user_id == user.id).first()
    if not entry:
        raise HTTPException(404, "Entry not found.")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(entry, field, value)
    db.commit()
    db.refresh(entry)
    return entry


@router.delete("/{entry_id}", status_code=204)
def delete_entry(entry_id: UUID, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    entry = db.query(JournalEntry).filter(JournalEntry.id == entry_id, JournalEntry.user_id == user.id).first()
    if not entry:
        raise HTTPException(404, "Entry not found.")
    db.delete(entry)
    db.commit()


@router.patch("/{entry_id}/favorite", response_model=EntryResponse)
def toggle_favorite(entry_id: UUID, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    entry = db.query(JournalEntry).filter(JournalEntry.id == entry_id, JournalEntry.user_id == user.id).first()
    if not entry:
        raise HTTPException(404, "Entry not found.")
    entry.is_favorite = not entry.is_favorite
    db.commit()
    db.refresh(entry)
    return entry
