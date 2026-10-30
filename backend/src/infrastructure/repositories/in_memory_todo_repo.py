"""Small in-memory repository used by unit tests."""

from src.domain.entities import TodoItem
from src.domain.repositories import ITodoRepository


class InMemoryTodoRepository(ITodoRepository):
    def __init__(self):
        self.items: dict[str, TodoItem] = {}

    def save(self, todo: TodoItem) -> None:
        self.items[todo.id] = todo

    def get_by_id(self, todo_id: str, owner_uid: str = "") -> TodoItem | None:
        todo = self.items.get(todo_id)
        if todo and owner_uid and todo.owner_uid != owner_uid:
            return None
        return todo

    def get_all(self) -> list[TodoItem]:
        return list(self.items.values())

    def get_by_owner(self, owner_uid: str) -> list[TodoItem]:
        return [todo for todo in self.items.values() if todo.owner_uid == owner_uid]

    def delete(self, todo_id: str, owner_uid: str = "") -> None:
        if self.get_by_id(todo_id, owner_uid):
            self.items.pop(todo_id)
