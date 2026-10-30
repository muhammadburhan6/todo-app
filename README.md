# Daymark Todo App

A simple full-stack todo application with user authentication, private task lists, filtering, editing, and dark mode.

## Features

- Email and password signup/login
- JWT-based session authentication
- Create, edit, complete, reopen, and delete todos
- All, active, and completed task filters
- User-specific MongoDB data
- Responsive light and dark interface

## Tech Stack

- **Frontend:** React and Vite
- **Backend:** FastAPI and Python
- **Database:** MongoDB
- **Authentication:** JWT with PBKDF2 password hashing

## Project Structure

```text
todo-app/
├── frontend/
│   └── src/
│       ├── components/
│       │   ├── Login.jsx
│       │   ├── Signup.jsx
│       │   └── TodoDashboard.jsx
│       ├── context/
│       ├── services/
│       ├── App.jsx
│       └── main.jsx
└── backend/
    ├── src/
    │   ├── application/
    │   ├── domain/
    │   ├── infrastructure/
    │   ├── presentation/
    │   └── shared/
    ├── tests/
    └── main.py
```

## Run Locally

### 1. Start MongoDB

Use local MongoDB on `mongodb://127.0.0.1:27017`, or provide a MongoDB Atlas connection string.

### 2. Start the backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
$env:JWT_SECRET = "replace-with-a-long-random-secret"
python -m uvicorn main:app --reload --port 8000
```

Optional backend settings:

```text
MONGODB_URI=mongodb://127.0.0.1:27017
MONGODB_DATABASE=daymark
JWT_SECRET=replace-with-a-long-random-secret
```

### 3. Start the frontend

```powershell
cd frontend
npm install
npm run dev
```

Open <http://localhost:5173>.

## Quality Checks

```powershell
cd backend
.\.venv\Scripts\python.exe -m pytest -q

cd ..\frontend
npm run lint
npm run build
```

## Author

Muhammad Burhan
