from src.application.dtos import CreateTodoCommand, TodoDTO
from src.application.mappers import todo_to_dto
from src.domain.entities import TodoItem
from src.domain.repositories import ITodoRepository
from src.domain.value_objects import Priority


class CreateTodoUseCase:
    def __init__(self, repository: ITodoRepository):
        self.repository = repository

    def execute(self, command: CreateTodoCommand) -> TodoDTO:
        todo = TodoItem.create(
            title=command.title,
            priority=Priority(command.priority.upper()),
            owner_uid=command.owner_uid,
        )
        self.repository.save(todo)
        return todo_to_dto(todo)
