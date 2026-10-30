from src.application.dtos import TodoDTO
from src.application.mappers import todo_to_dto
from src.domain.repositories import ITodoRepository


class ListTodosUseCase:
    def __init__(self, repository: ITodoRepository):
        self.repository = repository

    def execute(self, owner_uid: str) -> list[TodoDTO]:
        return [
            todo_to_dto(todo)
            for todo in self.repository.get_by_owner(owner_uid)
        ]
