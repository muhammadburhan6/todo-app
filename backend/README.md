# Daymark API

Simple FastAPI backend with MongoDB storage and JWT authentication.

## Structure

```text
backend/
├── main.py
├── src/
│   ├── application/      # Use cases
│   ├── domain/           # Business rules and contracts
│   ├── infrastructure/   # MongoDB repositories
│   ├── presentation/     # API routes and schemas
│   ├── shared/           # Security and logging helpers
│   ├── bootstrap.py      # Dependency setup
│   └── config.py         # Environment settings
└── tests/
```

## Setup

Requirements:

- Python 3.10+
- Local MongoDB or a MongoDB Atlas connection string

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
```

Optional settings:

| Variable | Default |
|---|---|
| `MONGODB_URI` | `mongodb://127.0.0.1:27017` |
| `MONGODB_DATABASE` | `daymark` |
| `JWT_SECRET` | Local development value |

Set a strong `JWT_SECRET` outside local development.

## Run

```powershell
python -m uvicorn main:app --reload --port 8000
```

- API: <http://127.0.0.1:8000>
- Swagger: <http://127.0.0.1:8000/docs>

## API

| Method | Endpoint | Purpose |
|---|---|---|
| `POST` | `/auth/signup` | Create an account |
| `POST` | `/auth/login` | Sign in and receive a JWT |
| `GET` | `/auth/me` | Restore the current session |
| `GET` | `/todos` | List the current user's todos |
| `POST` | `/todos` | Create a todo |
| `PATCH` | `/todos/{todo_id}` | Edit or toggle a todo |
| `DELETE` | `/todos/{todo_id}` | Delete a todo |

Protected routes use `Authorization: Bearer <token>`.

## Checks

```powershell
python -m pytest -q
```
