"""Authentication contract and its plain result objects."""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class UserData:
    uid: str
    email: str
    token: str


class IAuthRepository(ABC):
    @abstractmethod
    def create_user(
        self,
        email: str,
        password: str,
        display_name: str,
    ) -> UserData:
        """Register and return a user."""

    @abstractmethod
    def sign_in(self, email: str, password: str) -> UserData:
        """Check login details and return a signed access token."""
