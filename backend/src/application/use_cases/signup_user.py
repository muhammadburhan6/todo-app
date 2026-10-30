from dataclasses import dataclass

from src.domain.auth_repositories import IAuthRepository, UserData


@dataclass(frozen=True)
class SignupCommand:
    email: str
    password: str
    display_name: str


class SignupUserUseCase:
    def __init__(self, repository: IAuthRepository):
        self.repository = repository

    def execute(self, command: SignupCommand) -> UserData:
        return self.repository.create_user(
            command.email,
            command.password,
            command.display_name,
        )
