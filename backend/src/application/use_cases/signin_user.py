from dataclasses import dataclass

from src.domain.auth_repositories import IAuthRepository, UserData


@dataclass(frozen=True)
class SigninCommand:
    email: str
    password: str


class SigninUserUseCase:
    def __init__(self, repository: IAuthRepository):
        self.repository = repository

    def execute(self, command: SigninCommand) -> UserData:
        return self.repository.sign_in(command.email, command.password)
