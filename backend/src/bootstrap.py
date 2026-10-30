"""Create repositories and connect them to the application."""

from fastapi import FastAPI
from pymongo import MongoClient

from src.application.use_cases.create_todo import CreateTodoUseCase
from src.application.use_cases.delete_todo import DeleteTodoUseCase
from src.application.use_cases.list_todos import ListTodosUseCase
from src.application.use_cases.signin_user import SigninUserUseCase
from src.application.use_cases.signup_user import SignupUserUseCase
from src.application.use_cases.update_todo import UpdateTodoUseCase
from src.config import MONGODB_DATABASE, MONGODB_URI
from src.infrastructure.repositories.mongo_auth_repo import MongoAuthRepository
from src.infrastructure.repositories.mongo_todo_repo import MongoTodoRepository
from src.presentation.api.auth_router import get_signin_use_case, get_signup_use_case
from src.presentation.api.todo_router import (
    get_create_use_case,
    get_delete_use_case,
    get_list_use_case,
    get_update_use_case,
)


def wire_dependencies(app: FastAPI) -> None:
    """Build use cases and give them to FastAPI routes."""
    database = MongoClient(MONGODB_URI)[MONGODB_DATABASE]
    todo_repo = MongoTodoRepository(database.todos)
    auth_repo = MongoAuthRepository(database.users)

    create_use_case = CreateTodoUseCase(todo_repo)
    list_use_case = ListTodosUseCase(todo_repo)
    delete_use_case = DeleteTodoUseCase(todo_repo)
    update_use_case = UpdateTodoUseCase(todo_repo)
    signup_use_case = SignupUserUseCase(auth_repo)
    signin_use_case = SigninUserUseCase(auth_repo)

    app.dependency_overrides[get_create_use_case] = lambda: create_use_case
    app.dependency_overrides[get_list_use_case] = lambda: list_use_case
    app.dependency_overrides[get_delete_use_case] = lambda: delete_use_case
    app.dependency_overrides[get_update_use_case] = lambda: update_use_case
    app.dependency_overrides[get_signup_use_case] = lambda: signup_use_case
    app.dependency_overrides[get_signin_use_case] = lambda: signin_use_case
