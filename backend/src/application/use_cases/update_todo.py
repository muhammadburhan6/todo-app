from src.application.dtos import TodoDTO, UpdateTodoCommand
from src.application.mappers import todo_to_dto
from src.domain.exceptions import TodoNotFoundError
from src.domain.repositories import ITodoRepository


class UpdateTodoUseCase:
    def __init__(self, repository: ITodoRepository):
        self.repository = repository

    def execute(self, command: UpdateTodoCommand) -> TodoDTO:
        todo = self.repository.get_by_id(command.todo_id, command.owner_uid)
        if not todo:
            raise TodoNotFoundError("Todo not found.")

        todo.update(command.title, command.is_completed)
        self.repository.save(todo)
        return todo_to_dto(todo)
