"""MongoDB user storage with local password authentication."""

from uuid import uuid4

from pymongo.collection import Collection
from pymongo.errors import DuplicateKeyError

from src.domain.auth_repositories import IAuthRepository, UserData
from src.domain.exceptions import ValidationException
from src.shared.security import create_access_token, hash_password, verify_password


class MongoAuthRepository(IAuthRepository):
    def __init__(self, collection: Collection):
        self.collection = collection
        self._index_ready = False

    def _ensure_email_index(self) -> None:
        if not self._index_ready:
            self.collection.create_index("email", unique=True)
            self._index_ready = True

    def create_user(self, email: str, password: str, display_name: str) -> UserData:
        self._ensure_email_index()
        clean_email = email.strip().lower()
        uid = str(uuid4())

        try:
            self.collection.insert_one({
                "uid": uid,
                "email": clean_email,
                "display_name": display_name.strip() or "User",
                "password_hash": hash_password(password),
            })
        except DuplicateKeyError as error:
            raise ValidationException("An account with this email already exists.") from error

        return UserData(
            uid=uid,
            email=clean_email,
            token=create_access_token(uid, clean_email),
        )

    def sign_in(self, email: str, password: str) -> UserData:
        clean_email = email.strip().lower()
        user = self.collection.find_one({"email": clean_email})
        if not user or not verify_password(password, user.get("password_hash", "")):
            raise ValidationException("Invalid email or password.")

        return UserData(
            uid=user["uid"],
            email=user["email"],
            token=create_access_token(user["uid"], user["email"]),
        )
