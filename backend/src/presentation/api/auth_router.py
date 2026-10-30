from fastapi import APIRouter, Depends, HTTPException, status

from src.application.use_cases.signin_user import SigninCommand, SigninUserUseCase
from src.application.use_cases.signup_user import SignupCommand, SignupUserUseCase
from src.domain.exceptions import ValidationException
from src.presentation.api.auth_schemas import AuthResponse, LoginRequest, SignupRequest
from src.presentation.api.dependencies import CurrentUser, get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])


def get_signup_use_case() -> SignupUserUseCase:
    raise NotImplementedError


def get_signin_use_case() -> SigninUserUseCase:
    raise NotImplementedError


def auth_response(user, message: str) -> AuthResponse:
    return AuthResponse(
        uid=user.uid,
        email=user.email,
        token=user.token,
        message=message,
    )


@router.post("/signup", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def signup(
    request: SignupRequest,
    use_case: SignupUserUseCase = Depends(get_signup_use_case),
):
    try:
        user = use_case.execute(
            SignupCommand(request.email, request.password, request.display_name)
        )
        return auth_response(user, "User created successfully")
    except ValidationException as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@router.post("/login", response_model=AuthResponse)
def login(
    request: LoginRequest,
    use_case: SigninUserUseCase = Depends(get_signin_use_case),
):
    try:
        user = use_case.execute(SigninCommand(request.email, request.password))
        return auth_response(user, "Login successful")
    except ValidationException as error:
        raise HTTPException(status_code=401, detail=str(error)) from error


@router.get("/me")
def current_user(user: CurrentUser = Depends(get_current_user)):
    return {"uid": user.uid, "email": user.email}
