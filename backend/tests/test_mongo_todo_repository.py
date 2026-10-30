from src.domain.entities import TodoItem
from src.domain.value_objects import Priority
from src.infrastructure.repositories.mongo_todo_repo import MongoTodoRepository


class FakeCollection:
    def __init__(self):
        self.document = None

    def replace_one(self, query, document, upsert=False):
        self.document = document

    def find_one(self, query):
        if not self.document:
            return None
        if all(self.document.get(key) == value for key, value in query.items()):
            return self.document
        return None


def test_mongo_repository_converts_todo_to_document_and_back():
    repository = MongoTodoRepository(FakeCollection())
    todo = TodoItem.create(
        title="Keep the MongoDB adapter simple",
        priority=Priority.HIGH,
        owner_uid="user-123",
    )

    repository.save(todo)
    restored = repository.get_by_id(todo.id, todo.owner_uid)

    assert restored.id == todo.id
    assert restored.title == todo.title
    assert restored.priority == Priority.HIGH
    assert restored.owner_uid == "user-123"
