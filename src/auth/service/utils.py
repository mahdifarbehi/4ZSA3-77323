from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt.exceptions import InvalidTokenError
from auth.user import User
from backbone.base_exceptions import UnauthorizedException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from project_orm import DEFAULT_SESSION_FACTORY, TEST_SESSION_FACTORY
from unit_of_work import UnitOfWork
from auth.service.user_dto import UserDTO
from project_config import RUNNING_TESTS

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        token = request.headers.get("Authorization")
        request.state.token = token or None
        response = await call_next(request)
        return response


def get_current_username(token: Annotated[str, Depends(oauth2_scheme)]) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            raise UnauthorizedException()
        return username
    except InvalidTokenError as e:
        print(e)
        raise UnauthorizedException()


def get_current_user(request: Request) -> UserDTO:
    token = getattr(request.state, "token", None)
    if not token:
        raise UnauthorizedException()
    username = get_current_username(token)
    session_maker = (
        TEST_SESSION_FACTORY if RUNNING_TESTS == "TRUE" else DEFAULT_SESSION_FACTORY
    )
    with UnitOfWork(session_factory=session_maker) as uow:
        user: User | None = uow.session.query(User).filter_by(username=username).first()
        if user is None:
            raise UnauthorizedException()
        return UserDTO(id=user.id, username=user.username)
