import pytest

from src.application.dtos import CreateTodoCommand, DeleteTodoCommand, UpdateTodoCommand
from src.application.use_cases.create_todo import CreateTodoUseCase
from src.application.use_cases.delete_todo import DeleteTodoUseCase
from src.application.use_cases.update_todo import UpdateTodoUseCase
from src.domain.exceptions import TodoNotFoundError
from src.infrastructure.repositories.in_memory_todo_repo import InMemoryTodoRepository


@pytest.fixture
def repository():
    return InMemoryTodoRepository()


def create_todo(repository, owner_uid="owner-a"):
    return CreateTodoUseCase(repository).execute(
        CreateTodoCommand("Ship the polished workspace", "HIGH", owner_uid)
    )


def test_update_can_edit_complete_and_reopen_todo(repository):
    todo = create_todo(repository)
    use_case = UpdateTodoUseCase(repository)

    completed = use_case.execute(
        UpdateTodoCommand(todo.id, "owner-a", "Ship the simple workspace", True)
    )
    reopened = use_case.execute(UpdateTodoCommand(todo.id, "owner-a", is_completed=False))

    assert completed.title == "Ship the simple workspace"
    assert completed.completed_at is not None
    assert reopened.is_completed is False
    assert reopened.completed_at is None


def test_user_cannot_update_another_users_todo(repository):
    todo = create_todo(repository)

    with pytest.raises(TodoNotFoundError):
        UpdateTodoUseCase(repository).execute(
            UpdateTodoCommand(todo.id, "owner-b", is_completed=True)
        )


def test_delete_only_removes_owned_todo(repository):
    todo = create_todo(repository)

    with pytest.raises(TodoNotFoundError):
        DeleteTodoUseCase(repository).execute(DeleteTodoCommand(todo.id, "owner-b"))

    DeleteTodoUseCase(repository).execute(DeleteTodoCommand(todo.id, "owner-a"))
    assert repository.get_by_id(todo.id, "owner-a") is None
