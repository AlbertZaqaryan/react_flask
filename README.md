# 🚗 Car Inventory — React + FastAPI + MySQL

A full-stack CRUD application for managing a car inventory, fully containerized with Docker Compose.

## Stack

| Layer     | Tech                                   |
| --------- | -------------------------------------- |
| Frontend  | React 18 + Vite, served by nginx       |
| Backend   | FastAPI + SQLAlchemy (Python 3.12)     |
| Database  | MySQL 8.0                              |
| Infra     | Docker & Docker Compose                |

## Architecture

```
Browser ──► frontend (nginx :3000)
                │  /        → React SPA
                │  /api/*   → proxied to backend
                ▼
            backend (FastAPI :8000) ──► db (MySQL :3306)
```

## Features

- List, search, create, edit, and delete cars.
- Auto-seeded sample data on first startup.
- Server-side validation via Pydantic.
- REST API with interactive docs at `/docs`.

## Getting started

Requires Docker Desktop.

```bash
docker compose up --build
```

Then open:

- **App:** http://localhost:3000
- **API docs:** http://localhost:8000/docs
- **MySQL:** localhost:3307 (user/pass from `.env`)

To stop and remove volumes (wipes the database):

```bash
docker compose down -v
```

## API

Base path: `/api`

| Method | Path              | Description             |
| ------ | ----------------- | ----------------------- |
| GET    | `/health`         | Health check            |
| GET    | `/cars`           | List cars (`?search=`)  |
| GET    | `/cars/{id}`      | Get one car             |
| POST   | `/cars`           | Create a car            |
| PUT    | `/cars/{id}`      | Update a car            |
| DELETE | `/cars/{id}`      | Delete a car            |

### Example

```bash
curl -X POST http://localhost:8000/api/cars \
  -H "Content-Type: application/json" \
  -d '{"make":"Audi","model":"A4","year":2022,"color":"Grey","price":38000,"mileage":9000,"available":true}'
```

## Configuration

Database credentials live in `.env` (root). They are read by both the `db`
and `backend` services in `docker-compose.yml`.

## Local development (without Docker)

**Backend**

```bash
cd backend
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
# point DATABASE_URL at a running MySQL, then:
uvicorn app.main:app --reload
```

**Frontend**

```bash
cd frontend
npm install
npm run dev   # http://localhost:5173, proxies /api to :8000
```

## Project layout

```
.
├── docker-compose.yml
├── .env
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── main.py        # FastAPI app + routes
│       ├── database.py    # engine, session, db wait
│       ├── models.py      # SQLAlchemy Car model
│       ├── schemas.py     # Pydantic schemas
│       ├── crud.py        # DB operations
│       └── seed.py        # sample data
└── frontend/
    ├── Dockerfile         # build + nginx serve
    ├── nginx.conf         # SPA + /api proxy
    └── src/
        ├── App.jsx
        ├── api.js
        └── components/
```
