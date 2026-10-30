from fastapi import APIRouter, Depends, HTTPException, status

from src.application.dtos import CreateTodoCommand, DeleteTodoCommand, UpdateTodoCommand
from src.application.use_cases.create_todo import CreateTodoUseCase
from src.application.use_cases.delete_todo import DeleteTodoUseCase
from src.application.use_cases.list_todos import ListTodosUseCase
from src.application.use_cases.update_todo import UpdateTodoUseCase
from src.domain.exceptions import DomainError, TodoNotFoundError
from src.presentation.api.dependencies import CurrentUser, get_current_user
from src.presentation.api.schemas import CreateTodoRequest, TodoResponse, UpdateTodoRequest

router = APIRouter(prefix="/todos", tags=["Todos"])


def get_create_use_case() -> CreateTodoUseCase:
    raise NotImplementedError


def get_list_use_case() -> ListTodosUseCase:
    raise NotImplementedError


def get_update_use_case() -> UpdateTodoUseCase:
    raise NotImplementedError


def get_delete_use_case() -> DeleteTodoUseCase:
    raise NotImplementedError


@router.get("", response_model=list[TodoResponse])
def list_todos(
    user: CurrentUser = Depends(get_current_user),
    use_case: ListTodosUseCase = Depends(get_list_use_case),
):
    return use_case.execute(user.uid)


@router.post("", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo(
    request: CreateTodoRequest,
    user: CurrentUser = Depends(get_current_user),
    use_case: CreateTodoUseCase = Depends(get_create_use_case),
):
    try:
        return use_case.execute(
            CreateTodoCommand(request.title, request.priority, user.uid)
        )
    except DomainError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@router.patch("/{todo_id}", response_model=TodoResponse)
def update_todo(
    todo_id: str,
    request: UpdateTodoRequest,
    user: CurrentUser = Depends(get_current_user),
    use_case: UpdateTodoUseCase = Depends(get_update_use_case),
):
    try:
        return use_case.execute(
            UpdateTodoCommand(
                todo_id=todo_id,
                owner_uid=user.uid,
                title=request.title,
                is_completed=request.is_completed,
            )
        )
    except TodoNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    except DomainError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(
    todo_id: str,
    user: CurrentUser = Depends(get_current_user),
    use_case: DeleteTodoUseCase = Depends(get_delete_use_case),
):
    try:
        use_case.execute(DeleteTodoCommand(todo_id, user.uid))
    except TodoNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
