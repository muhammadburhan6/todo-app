from src.infrastructure.repositories.mongo_auth_repo import MongoAuthRepository


class FakeUsers:
    def __init__(self):
        self.user = None

    def create_index(self, field, unique=False):
        return field

    def insert_one(self, user):
        self.user = user

    def find_one(self, query):
        if self.user and self.user["email"] == query["email"]:
            return self.user
        return None


def test_mongo_auth_repository_can_signup_and_login():
    users = FakeUsers()
    repository = MongoAuthRepository(users)

    created = repository.create_user("USER@example.com", "password123", "User")
    signed_in = repository.sign_in("user@example.com", "password123")

    assert created.email == "user@example.com"
    assert signed_in.uid == created.uid
    assert signed_in.token
    assert users.user["password_hash"] != "password123"
