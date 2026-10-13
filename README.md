# Document AI

Document AI - hujjatlarni yuklab, matn ajratib, AI bilan tahlil qiluvchi tizim.

## Texnologiyalar

- **Backend:** FastAPI + SQLAlchemy + Alembic + PostgreSQL
- **Task Queue:** Celery + Redis
- **Frontend:** React + Vite + Tailwind CSS
- **OCR:** Tesseract
- **AI:** Groq API
- **Platform:** Windows

## Ishga tushirish

### 1. Docker (Postgres va Redis)

```bash
docker compose up -d
```

Tekshirish:
```bash
docker compose ps
docker exec document_ai_redis redis-cli ping  # PONG
```

### 2. Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend http://127.0.0.1:8000 da ishlaydi.
- Health check: http://127.0.0.1:8000/health
- API docs: http://127.0.0.1:8000/docs

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend http://localhost:5173 da ishlaydi.

## Environment Variables

`.env` faylini yaratish (backend papkasida):

```env
DATABASE_URL=postgresql://document_ai:document_ai_password@localhost:5432/document_ai
REDIS_URL=redis://localhost:6379/0
UPLOAD_DIR=../uploads
MAX_UPLOAD_MB=50
GROQ_API_KEY=your_groq_api_key_here
```

## Papkalar tuzilishi

```
document_ai/
├── backend/
│   ├── app/
│   │   ├── models/
│   │   ├── routers/
│   │   ├── services/
│   │   └── tasks/
│   ├── tests/
│   └── requirements.txt
├── frontend/
│   ├── src/
│   └── package.json
├── uploads/
├── docker-compose.yml
└── .env
```

## Development

- Backend: FastAPI + SQLAlchemy
- Frontend: React + Tailwind CSS
- Database migrations: Alembic
- Background tasks: Celery
