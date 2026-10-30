from src.application.use_cases.create_todo import CreateTodoUseCase
from src.application.use_cases.delete_todo import DeleteTodoUseCase
from src.application.use_cases.list_todos import ListTodosUseCase
from src.application.use_cases.update_todo import UpdateTodoUseCase
from src.infrastructure.repositories.in_memory_todo_repo import InMemoryTodoRepository
from src.presentation.api.dependencies import CurrentUser
from src.presentation.api.schemas import CreateTodoRequest, UpdateTodoRequest
from src.presentation.api.todo_router import create_todo, delete_todo, list_todos, update_todo


def test_todo_routes_work_together():
    repository = InMemoryTodoRepository()
    user = CurrentUser(uid="user-1", email="user@example.com")

    todo = create_todo(
        CreateTodoRequest(title="Test the complete todo flow", priority="HIGH"),
        user,
        CreateTodoUseCase(repository),
    )
    updated = update_todo(
        todo.id,
        UpdateTodoRequest(is_completed=True),
        user,
        UpdateTodoUseCase(repository),
    )

    assert updated.is_completed is True
    assert [item.id for item in list_todos(user, ListTodosUseCase(repository))] == [todo.id]

    delete_todo(todo.id, user, DeleteTodoUseCase(repository))
    assert list_todos(user, ListTodosUseCase(repository)) == []
