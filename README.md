# Pastebin-Lite

A minimal Pastebin-like web application where users can create text pastes and share a link to view them. Pastes can optionally expire by **time (TTL)** or **view count**. This project is built as a take-home assessment focusing on backend correctness, persistence, and constraint handling rather than UI design.

---

## Tech Stack

**Backend**
- Python
- FastAPI
- SQLAlchemy Core
- PostgreSQL (Neon free tier)
- Jinja2 (HTML rendering)

**Frontend**
- React (Vite)
- React Router
- Fetch API

**Deployment**
- Frontend: Vercel
- Backend: Railway / Fly.io / Render
- Database: Neon PostgreSQL

---

## Features

- Create a paste with arbitrary text
- Optional TTL expiry
- Optional max view limit
- Shareable URL generation
- HTML paste viewing
- Safe content rendering (no script execution)
- Deterministic time testing support
- Concurrency-safe view counting
- Health check endpoint

---

## API Endpoints

| Method | Route | Description |
|-------|------|-------------|
| GET | `/api/healthz` | Health check |
| POST | `/api/pastes` | Create paste |
| GET | `/api/pastes/:id` | Fetch paste (JSON) |
| GET | `/p/:id` | View paste (HTML) |

---

## Environment Variables

**Backend**
DATABASE_URL=postgresql://user:pass@host/db
BASE_URL=https://your-backend-domain.com
TEST_MODE=1


**Frontend**
VITE_API_URL=https://your-backend-domain.com


---

## Running Locally

**Backend**
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
Backend runs at `http://127.0.0.1:8000`

**Frontend**
cd frontend
npm install
npm run dev
Frontend runs at `http://localhost:5173`

---

## Persistence Layer

PostgreSQL is used for data storage to ensure:
- Data survives across requests
- Serverless compatibility
- Atomic view updates
- Concurrency safety
- Deterministic TTL handling

Neon’s free tier PostgreSQL is used for development and testing.

---

## Important Design Decisions

- **View Counting:** Uses database transactions with row locking to avoid race conditions.
- **Expiry Handling:** Supports deterministic time via `x-test-now-ms` header when `TEST_MODE=1`.
- **Security:** Paste content is escaped before HTML rendering.
- **No In-Memory Storage:** Prevents data loss on serverless cold starts.
- **Minimal UI:** Focused on functional correctness rather than styling.

---

## Notes

- UI styling is intentionally simple.
- No secrets or credentials are committed to the repository.
- No hardcoded localhost URLs in production code.
- All API responses return valid JSON with proper status codes.
- HTML rendering is safe against script injection.

---

## Estimated Build Time

Approximately 3–4 hours including backend, frontend, and deployment.
