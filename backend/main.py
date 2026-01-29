from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select, insert, update, text
from sqlalchemy.exc import SQLAlchemyError
from datetime import timedelta
from db import engine, SessionLocal, metadata
from models import pastes
from schemas import PasteCreate, PasteResponse, PasteFetchResponse
from utils import generate_id, get_now
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_URL = os.getenv("BASE_URL", "https://your-app.vercel.app")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def startup():
    metadata.create_all(engine)

# ---------- HEALTH ----------
@app.get("/api/healthz")
def health(db=Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"ok": True}
    except:
        return JSONResponse(status_code=500, content={"ok": False})

# ---------- CREATE ----------
@app.post("/api/pastes", response_model=PasteResponse)
def create_paste(body: PasteCreate, request: Request, db=Depends(get_db)):
    now = get_now(request)
    paste_id = generate_id()

    expires_at = (
        now + timedelta(seconds=body.ttl_seconds)
        if body.ttl_seconds else None
    )

    stmt = insert(pastes).values(
        id=paste_id,
        content=body.content,
        created_at=now,
        expires_at=expires_at,
        max_views=body.max_views,
        view_count=0
    )

    db.execute(stmt)
    db.commit()

    return {
        "id": paste_id,
        "url": f"{BASE_URL}/p/{paste_id}"
    }

# ---------- FETCH API ----------
@app.get("/api/pastes/{paste_id}", response_model=PasteFetchResponse)
def fetch_paste(paste_id: str, request: Request, db=Depends(get_db)):
    now = get_now(request)

    try:
        db.execute(text("BEGIN"))

        row = db.execute(
            select(pastes).where(pastes.c.id == paste_id).with_for_update()
        ).fetchone()

        if not row:
            raise HTTPException(404, "Not found")

        # Expiry
        if row.expires_at and now > row.expires_at:
            raise HTTPException(404, "Expired")

        # Views
        if row.max_views is not None and row.view_count >= row.max_views:
            raise HTTPException(404, "View limit exceeded")

        # Increment
        db.execute(
            update(pastes)
            .where(pastes.c.id == paste_id)
            .values(view_count=row.view_count + 1)
        )

        db.commit()

        remaining = None
        if row.max_views is not None:
            remaining = row.max_views - (row.view_count + 1)

        return {
            "content": row.content,
            "remaining_views": remaining,
            "expires_at": row.expires_at.isoformat() if row.expires_at else None
        }

    except HTTPException as e:
        db.rollback()
        raise e
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(500, "DB Error")
    now = get_now(request)

    row = db.execute(
        select(pastes).where(pastes.c.id == paste_id)
    ).fetchone()

    if not row:
        raise HTTPException(404)

    if row.expires_at and now > row.expires_at:
        raise HTTPException(404)

    if row.max_views is not None and row.view_count >= row.max_views:
        raise HTTPException(404)

    return template.render(content=row.content)
