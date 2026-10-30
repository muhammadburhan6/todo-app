"""MongoDB implementation of the todo repository."""

from datetime import datetime
from typing import List, Optional

from pymongo.collection import Collection

from src.domain.entities import TodoItem
from src.domain.repositories import ITodoRepository
from src.domain.value_objects import Priority, TaskTitle


class MongoTodoRepository(ITodoRepository):
    def __init__(self, collection: Collection):
        self.collection = collection

    @staticmethod
    def _to_document(todo: TodoItem) -> dict:
        return {
            "id": todo.id,
            "title": todo.title.value,
            "priority": todo.priority.value,
            "is_completed": todo.is_completed,
            "owner_uid": todo.owner_uid,
            "created_at": todo.created_at,
            "completed_at": todo.completed_at,
        }

    @staticmethod
    def _to_entity(document: dict) -> TodoItem:
        return TodoItem(
            id=document["id"],
            title=TaskTitle(document["title"]),
            priority=Priority(document["priority"]),
            is_completed=document["is_completed"],
            owner_uid=document["owner_uid"],
            created_at=document["created_at"],
            completed_at=document.get("completed_at"),
        )

    def save(self, todo: TodoItem) -> None:
        self.collection.replace_one(
            {"id": todo.id, "owner_uid": todo.owner_uid},
            self._to_document(todo),
            upsert=True,
        )

    def get_by_id(self, todo_id: str, owner_uid: str = "") -> Optional[TodoItem]:
        query = {"id": todo_id}
        if owner_uid:
            query["owner_uid"] = owner_uid
        document = self.collection.find_one(query)
        return self._to_entity(document) if document else None

    def get_all(self) -> List[TodoItem]:
        return [self._to_entity(item) for item in self.collection.find()]

    def get_by_owner(self, owner_uid: str) -> List[TodoItem]:
        documents = self.collection.find({"owner_uid": owner_uid}).sort(
            "created_at",
            -1,
        )
        return [self._to_entity(item) for item in documents]

    def delete(self, todo_id: str, owner_uid: str = "") -> None:
        query = {"id": todo_id}
        if owner_uid:
            query["owner_uid"] = owner_uid
        self.collection.delete_one(query)
