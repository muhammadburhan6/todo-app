from src.application.dtos import DeleteTodoCommand
from src.domain.exceptions import TodoNotFoundError
from src.domain.repositories import ITodoRepository


class DeleteTodoUseCase:
    def __init__(self, repository: ITodoRepository):
        self.repository = repository

    def execute(self, command: DeleteTodoCommand) -> None:
        if not self.repository.get_by_id(command.todo_id, command.owner_uid):
            raise TodoNotFoundError("Todo not found.")
        self.repository.delete(command.todo_id, command.owner_uid)
