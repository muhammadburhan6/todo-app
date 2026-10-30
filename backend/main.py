"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.bootstrap import wire_dependencies
from src.presentation.api.auth_router import router as auth_router
from src.presentation.api.todo_router import router as todo_router


def health_check():
    return {"status": "ok"}


def create_app() -> FastAPI:
    """Build and return the configured FastAPI application."""
    application = FastAPI(
        title="Daymark API",
        description="Todo API with MongoDB and JWT authentication.",
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    wire_dependencies(application)

    application.include_router(auth_router)
    application.include_router(todo_router)
    application.add_api_route(
        "/",
        health_check,
        methods=["GET"],
        tags=["Health"],
    )
    return application


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
