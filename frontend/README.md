# Daymark frontend

A React + Vite interface for the FastAPI Todo service in this repository.

## Structure

```text
src/
├── components/
│   ├── Login.jsx
│   ├── Signup.jsx
│   └── TodoDashboard.jsx
├── context/
│   ├── AuthContext.jsx
│   └── ThemeContext.jsx
├── services/
│   └── api.js
├── App.jsx
├── main.jsx
└── styles.css
```

## Run locally

1. Start the FastAPI backend from the `backend` directory on `http://127.0.0.1:8000`.
2. In this `frontend` directory, install dependencies:

   ```bash
   npm install
   ```

3. Start the Vite development server:

   ```bash
   npm run dev
   ```

4. Open `http://localhost:5173` in your browser.

Vite proxies `/auth` and `/todos` to FastAPI, so no frontend API environment variable is required for development.

## Quality checks

```bash
npm run lint
npm run build
```

The authentication token is stored in the browser's local storage to match the current backend contract. Protected `401` responses clear the stored token and return the user to the login screen.
