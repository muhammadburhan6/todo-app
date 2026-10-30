"""Todo entity and its business rules.

The domain stays independent from FastAPI and database details.
"""

from dataclasses import dataclass
from datetime import datetime, timezone
import uuid

from src.domain.value_objects import Priority, TaskTitle


@dataclass
class TodoItem:
    """Main business object for one todo."""

    id: str
    title: TaskTitle
    priority: Priority
    is_completed: bool
    created_at: datetime
    owner_uid: str = ""
    completed_at: datetime | None = None

    @classmethod
    def create(
        cls,
        title: str,
        priority: Priority = Priority.MEDIUM,
        owner_uid: str = "",
    ) -> "TodoItem":
        """Create a new valid todo with an id and time."""
        return cls(
            id=str(uuid.uuid4()),
            title=TaskTitle(title),
            priority=priority,
            is_completed=False,
            created_at=datetime.now(timezone.utc),
            owner_uid=owner_uid,
            completed_at=None,
        )

    def update(self, title: str | None = None, is_completed: bool | None = None) -> None:
        """Apply editable fields while keeping domain values valid."""
        if title is not None:
            self.title = TaskTitle(title)

        if is_completed is not None and is_completed != self.is_completed:
            self.is_completed = is_completed
            self.completed_at = datetime.now(timezone.utc) if is_completed else None
