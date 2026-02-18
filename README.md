# memento-api

FastAPI backend for the Memento journaling app. Uses PostgreSQL for persistence and JWT for authentication.

## Stack

- **Python** 3.11+
- **FastAPI** + Uvicorn
- **PostgreSQL** 16 (via Docker)
- **SQLAlchemy** 2.0 (ORM)
- **JWT** authentication (python-jose + passlib)

## Prerequisites

- [Docker](https://www.docker.com/) and Docker Compose
- Python 3.11+ (only needed for the non-Docker local setup)

## Running Locally (Docker — recommended)

This is the easiest way. Docker Compose will spin up PostgreSQL, the FastAPI app, and pgAdmin together.

### 1. Clone the repo

```bash
git clone https://github.com/alexandredewaele/memento-api.git
cd memento-api
```

### 2. Set up environment variables

```bash
cp .env.example .env
```

Edit `.env` and replace `SECRET_KEY` with a securely generated value:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 3. Start the services

```bash
docker compose up --build
```

This will start:

| Service  | URL                          | Description              |
|----------|------------------------------|--------------------------|
| API      | http://localhost:8000        | FastAPI backend          |
| Docs     | http://localhost:8000/docs   | Swagger UI               |
| pgAdmin  | http://localhost:5050        | DB admin UI              |

### 4. Stop the services

```bash
docker compose down
```

To also remove the database volume (wipes all data):

```bash
docker compose down -v
```

---

## Running Locally (without Docker)

Use this if you want to run the API directly with a local Python environment.

### 1. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up environment variables

```bash
cp .env.example .env
```

Edit `.env` and set `DATABASE_URL` to point to your local PostgreSQL instance:

```
DATABASE_URL=postgresql://your_user:your_password@localhost:5432/memento_db
```

### 4. Run the development server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## API Overview

| Method | Endpoint                  | Description              | Auth required |
|--------|---------------------------|--------------------------|---------------|
| POST   | `/api/auth/register`      | Register a new user      | No            |
| POST   | `/api/auth/login`         | Login, returns JWT token | No            |
| GET    | `/api/auth/me`            | Get current user info    | Yes           |
| GET    | `/api/entries`            | List all entries         | Yes           |
| POST   | `/api/entries`            | Create a new entry       | Yes           |
| PUT    | `/api/entries/{id}`       | Update an entry          | Yes           |
| DELETE | `/api/entries/{id}`       | Delete an entry          | Yes           |
| PATCH  | `/api/entries/{id}/favorite` | Toggle favorite       | Yes           |

Full interactive docs available at **http://localhost:8000/docs** when the server is running.

## Environment Variables

| Variable                    | Description                                      | Default                  |
|-----------------------------|--------------------------------------------------|--------------------------|
| `DATABASE_URL`              | PostgreSQL connection string                     | *(required)*             |
| `SECRET_KEY`                | Secret key for JWT signing                       | *(required)*             |
| `ALGORITHM`                 | JWT algorithm                                    | `HS256`                  |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiry in minutes                        | `1440` (24h)             |
| `ALLOWED_ORIGINS`           | Comma-separated list of allowed CORS origins     | `http://localhost:5173`  |
